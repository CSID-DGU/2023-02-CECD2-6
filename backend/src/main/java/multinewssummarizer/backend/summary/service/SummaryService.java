package multinewssummarizer.backend.summary.service;

import lombok.RequiredArgsConstructor;
import multinewssummarizer.backend.global.exceptionhandler.CustomExceptions;
import multinewssummarizer.backend.news.domain.News;
import multinewssummarizer.backend.news.repository.NewsRepository;
import multinewssummarizer.backend.summary.domain.Batchresult;
import multinewssummarizer.backend.summary.domain.Summarizelog;
import multinewssummarizer.backend.summary.model.*;
import multinewssummarizer.backend.summary.repository.BatchresultRepository;
import multinewssummarizer.backend.summary.repository.SummarizelogRepository;
import multinewssummarizer.backend.user.domain.Users;
import multinewssummarizer.backend.user.repository.UserRepository;
//import org.json.JSONObject;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.RestTemplate;

import java.time.LocalDateTime;
import java.util.*;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class SummaryService {

    private final UserRepository userRepository;
    private final SummarizelogRepository summarizeLogRepository;
    private final NewsRepository newsRepository;
    private final BatchresultRepository batchResultRepository;

    private static String url = "https://dd24-116-255-71-186.ngrok-free.app/summary/";

    @Transactional
    public SummaryResponseDto instantSummary(SummaryRequestDto summaryRequestDto) throws ParseException {
        System.out.println("summaryRequestDto = " + summaryRequestDto);
        ArrayList<String> categories = summaryRequestDto.getCategories();
        ArrayList<String> keywords = summaryRequestDto.getKeywords();
        LocalDateTime oneDayAgo = LocalDateTime.now().minusDays(1);

        if (categories.isEmpty()) {
            categories = null;
        }
        if (keywords.isEmpty()) {
            keywords = null;
        }

        List<SummaryRepositoryVO> findNews = newsRepository.findNewsByCategoriesAndKeywords(categories, keywords, oneDayAgo);
        System.out.println("findNews = " + findNews);
        if (findNews.isEmpty()) {
            throw new CustomExceptions.NoNewsDataException("선택한 주제/키워드에 해당하는 뉴스 데이터가 존재하지 않습니다.");
        }
        List<Long> findIds = new ArrayList<>();
        List<String> links = new ArrayList<>();
        List<String> titles = new ArrayList<>();
        List<String> contexts = new ArrayList<>();
        for (SummaryRepositoryVO summaryRepositoryVO : findNews) {
            findIds.add(summaryRepositoryVO.getId());
            links.add(summaryRepositoryVO.getLink());
            titles.add(summaryRepositoryVO.getTitle());
            contexts.add(summaryRepositoryVO.getContext());
        }

        // POST 요청
        RestTemplate rt = new RestTemplate();
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        JSONObject bodies = new JSONObject();
        bodies.put("numbers", findIds);
        HttpEntity<String> entity = new HttpEntity<>(bodies.toString(), headers);
        String response = rt.postForObject(url, entity, String.class);

        JSONParser jsonParser = new JSONParser();
        JSONObject jsonObject = (JSONObject) jsonParser.parse(response);
        String summary =jsonObject.get("summary").toString();

        String strNewsIds = convertToString((ArrayList<Long>) findIds);
        String strCategories = convertToString(categories);
        String strKeywords = convertToString(keywords);

        Users findUser = userRepository.findById(summaryRequestDto.getUserId()).get();
        Summarizelog summarizeLog = Summarizelog.builder()
                .users(findUser)
                .summarize(summary)
                .categories(strCategories)
                .keywords(strKeywords)
                .newsIds(strNewsIds)
                .createdTime(LocalDateTime.now())
                .batchNewsId(null)
                .build();
        summarizeLogRepository.save(summarizeLog);

        /**
         * TODO: 만약, 오류가 발생했을 시, postForObject()로 시도한다면 에러세시지가 뜨지 않지만, exchange()로 한다면, <200 OK OK,{summary=}>로 뜬다. exception처리가 필요할수도
         */

        SummaryResponseDto summaryResponseDto = SummaryResponseDto.builder()
                .ids(findIds)
                .links(links)
                .titles(titles)
                .contexts(contexts)
                .summary(summary)
                .build();

        return summaryResponseDto;
    }

    @Transactional
    public boolean batchSummary() throws ParseException{
        // 1. 모든 유저에 대해서
        List<Users> userlist = userRepository.findAll();
        System.out.println("userlist = " + userlist);

        // 2. 유저가 설정한 주제와 키워드들을 불러오고
        for(Users u : userlist){
            String userTopics = u.getTopics();
            String userKeywords = u.getKeywords();
            ArrayList<String> categories = null;
            ArrayList<String> keywords = null;
            // 2-1. 주제와 키워드들을 추가
            if(userTopics!=null){
                categories = new ArrayList<>();
                Collections.addAll(categories,userTopics.split(","));
            }
            if(userKeywords!=null){
                keywords = new ArrayList<>();
                Collections.addAll(keywords,userKeywords.split(","));
            }
            if(categories==null && keywords==null){
                continue;
            }

            // TMP
            System.out.println("categories = " + categories);
            System.out.println("keywords = " + keywords);

            LocalDateTime oneDayAgo = LocalDateTime.now().minusDays(1);
            List<SummaryRepositoryVO> findNews = newsRepository.findNewsByCategoriesAndKeywords(categories, keywords, oneDayAgo);
            System.out.println("findNews = " + findNews);
            // 부합하는 뉴스가 없으면 스킵
            if (findNews.isEmpty()) {
                continue;
            }
            List<Long> findIds = new ArrayList<>();
            List<String> contexts = new ArrayList<>();
            for (SummaryRepositoryVO summaryRepositoryVO : findNews) {
                findIds.add(summaryRepositoryVO.getId());
                contexts.add(summaryRepositoryVO.getContext());
            }

            // 4. 키워드 전체에 대한 요약문을 만들고
            // POST 요청
            RestTemplate rt = new RestTemplate();
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            JSONObject bodies = new JSONObject();
            bodies.put("numbers", findIds);
            HttpEntity<String> entity = new HttpEntity<>(bodies.toString(), headers);
            String response = rt.postForObject(url, entity, String.class);

            JSONParser jsonParser = new JSONParser();
            JSONObject jsonObject = (JSONObject) jsonParser.parse(response);
            String summary=jsonObject.get("summary").toString();

            String strNewsIds = convertToString((ArrayList<Long>) findIds);

            // 5. DB의 BatchResult 테이블에 저장한다
            Batchresult batchResult = Batchresult.builder()
                    .users(u)
                    .summarize(summary)
                    .categories(userTopics)
                    .keywords(userKeywords)
                    .newsIds(strNewsIds)
                    .createdTime(LocalDateTime.now())
                    .build();
            batchResultRepository.save(batchResult);
        }
        return true;
    }

    @Transactional
    public BatchSummaryResponseDto getLastBatchSummary(Long id) {
        Users findUser = userRepository.findById(id).get();
        Optional<Batchresult> result = batchResultRepository.findLastSummaryByUserId(findUser);

        if(result.isEmpty()) {
            throw new CustomExceptions.NoBatchNewsDataException("요약된 뉴스 데이터가 존재하지 않습니다.");
        }

        Batchresult batchResult = result.get();

        String strRawNewsIds = batchResult.getNewsIds();
        String[] strNewsIds = strRawNewsIds.split(",");

        List<Long> newsIds = new ArrayList<>();

        for (String strNewsId: strNewsIds) {
            newsIds.add(Long.parseLong(strNewsId));
        }

        List<News> newses = newsRepository.findAllById(newsIds);

        List<SummaryNewsVO> summaryNewsVO = new ArrayList<>();

        for (News news: newses) {
            summaryNewsVO.add(SummaryNewsVO.builder()
                    .title(news.getTitle())
                    .context(news.getContext())
                    .companyName(news.getCompanyName())
                    .link(news.getLink())
                    .build());
        }

        // Summarylog에 해당 데이터가 이미 저장되어있는지 확인. 없다면 SummarizeLog에 추가
        if(summarizeLogRepository.findByBatchnewsId(batchResult.getId()).isEmpty()) {
            Summarizelog summarizelog = Summarizelog.builder()
                    .users(findUser)
                    .summarize(batchResult.getSummarize())
                    .categories(batchResult.getCategories())
                    .keywords(batchResult.getKeywords())
                    .newsIds(batchResult.getNewsIds())
                    .createdTime(batchResult.getCreatedTime())
                    .batchNewsId(batchResult.getId())
                    .build();

            summarizeLogRepository.save(summarizelog);
        }

        BatchSummaryResponseDto batchSummaryResponseDto = BatchSummaryResponseDto.builder()
                .summary(batchResult.getSummarize())
                .news(summaryNewsVO)
                .build();

        return batchSummaryResponseDto;
    }

    @Transactional
    public List<SummaryLogsResponseDto> getUserSummaryLogs(Long id) {
        Users findUser = userRepository.findById(id).get();
        List<Summarizelog> findSummarizeLogs = summarizeLogRepository.findByUsers(findUser);

        if (findSummarizeLogs.isEmpty()) {
            throw new CustomExceptions.NoSummaryLogException("요약 결과가 존재하지 않습니다.");
        }

        List<SummaryLogsResponseDto> response = new ArrayList<>();
        for (Summarizelog findSummarizeLog : findSummarizeLogs) {
            String strRawNewsIds = findSummarizeLog.getNewsIds();
            String[] strNewsIds = strRawNewsIds.split(",");

            List<SummaryNewsVO> summaryNewsVOList = new ArrayList<>();
            for (String strNewsId : strNewsIds) {
                News news = newsRepository.findById(Long.parseLong(strNewsId)).get();

                summaryNewsVOList.add(SummaryNewsVO.builder()
                        .title(news.getTitle())
                        .context(news.getContext())
                        .companyName(news.getCompanyName())
                        .link(news.getLink())
                        .build());
            }

            response.add(SummaryLogsResponseDto.builder()
                    .summary(findSummarizeLog.getSummarize())
                    .categories(findSummarizeLog.getCategories())
                    .keywords(findSummarizeLog.getKeywords())
                    .createdTime(findSummarizeLog.getCreatedTime())
                    .news(summaryNewsVOList)
                    .build());
        }


        return response;
    }

    private <T> String convertToString(ArrayList<T> list) {
        if(list == null) {
            return null;
        }
        else {
            StringBuilder convert = new StringBuilder();
            for (T element : list) {
                convert.append(element).append(",");
            }
            if (convert.length() > 0) {
                convert.deleteCharAt(convert.length() - 1); // 마지막 콤마 제거
            }
            return convert.toString();
        }
    }

}
