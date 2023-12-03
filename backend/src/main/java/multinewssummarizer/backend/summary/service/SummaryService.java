package multinewssummarizer.backend.summary.service;

import lombok.RequiredArgsConstructor;
import multinewssummarizer.backend.global.exceptionhandler.CustomExceptions;
import multinewssummarizer.backend.news.repository.NewsRepository;
import multinewssummarizer.backend.summary.domain.Summarize;
import multinewssummarizer.backend.summary.model.SummaryRequestDto;
import multinewssummarizer.backend.summary.model.SummaryResponseDto;
import multinewssummarizer.backend.summary.model.SummaryRepositoryVO;
import multinewssummarizer.backend.summary.repository.SummarizeRepository;
import multinewssummarizer.backend.user.domain.Users;
import multinewssummarizer.backend.user.repository.UserRepository;
//import org.json.JSONObject;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import org.springframework.boot.json.JsonParser;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class SummaryService {

    private final UserRepository userRepository;
    private final SummarizeRepository summarizeRepository;
    private final NewsRepository newsRepository;

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
        for (SummaryRepositoryVO summaryRepositoryVO : findNews) {
            findIds.add(summaryRepositoryVO.getId());
            links.add(summaryRepositoryVO.getLink());
            titles.add(summaryRepositoryVO.getTitle());
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

        String strCategories = convertToString(categories);
        String strKeywords = convertToString(keywords);

        Users findUser = userRepository.findById(summaryRequestDto.getUserId()).get();
        Summarize summarize = Summarize.builder()
                .users(findUser)
                .summarize(summary)
                .categories(strCategories)
                .keywords(strKeywords)
                .build();
        summarizeRepository.save(summarize);

        /**
         * TODO: 만약, 오류가 발생했을 시, postForObject()로 시도한다면 에러세시지가 뜨지 않지만, exchange()로 한다면, <200 OK OK,{summary=}>로 뜬다. exception처리가 필요할수도
         */

        SummaryResponseDto summaryResponseDto = SummaryResponseDto.builder()
                .ids(findIds)
                .links(links)
                .titles(titles)
                .summary(summary)
                .build();

        return summaryResponseDto;
    }

//    @Transactional
//    public SummaryResponseDto testSummary(List<Long> ids) throws ParseException {
//        // POST 요청
//        RestTemplate rt2 = new RestTemplate();
//        HttpHeaders headers = new HttpHeaders();
//        headers.setContentType(MediaType.APPLICATION_JSON);
//        JSONObject body = new JSONObject();
//        body.put("numbers", ids);
//
//        HttpEntity<String> entity = new HttpEntity<>(body.toString(), headers);
//
////            ResponseEntity<?> responseBody = rt2.exchange(url, HttpMethod.POST, entity, Object.class);
//        String responseBody = rt2.postForObject(url, entity, String.class);
//        System.out.println("responseBody = " + responseBody);
//
//        JSONParser jsonParser = new JSONParser();
//        JSONObject jsonObject = (JSONObject) jsonParser.parse(responseBody.toString());
//        String summary = jsonObject.get("summary").toString();
//
//        ArrayList<String> categories = new ArrayList<>();
//        categories.add("정치");
//        categories.add("경제");
//
//        ArrayList<String> keywords = new ArrayList<>();
//        keywords = null;
//
//        Long userId = 37L;
//        String strCategories = convertToString(categories);
//        String strKeywords = convertToString(keywords);
//
//        Users findUser = userRepository.findById(userId).get();
//        Summarize summarize = Summarize.builder()
//                .users(findUser)
//                .summarize(summary)
//                .categories(strCategories)
//                .keywords(strKeywords)
//                .build();
//        summarizeRepository.save(summarize);
//
//        SummaryResponseDto summaryResponseDto = SummaryResponseDto.builder()
//                .ids(ids)
//                .links(null)
//                .titles(null)
//                .summary(summary)
//                .build();
//
//
//        return summaryResponseDto;
//
//    }

    private String convertToString(ArrayList<String> list) {
        if(list == null) {
            return null;
        }
        else {
            String convert = "";
            for (String l : list) {
                convert += l;
                convert += ",";
            }
            String result = convert.substring(0, convert.length() - 1);
            return result;
        }
    }

}
