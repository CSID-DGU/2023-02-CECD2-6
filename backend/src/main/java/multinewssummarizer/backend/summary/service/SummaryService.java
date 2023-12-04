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
import multinewssummarizer.backend.summary.model.UserSummaryResponseDto;
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
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

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

    @Transactional
    public List<UserSummaryResponseDto> getUserSummaryLogs(Long id) {
        Users findUser = userRepository.findById(id).get();
        List<Summarize> findSummarizes = summarizeRepository.findByUsers(findUser);

        List<UserSummaryResponseDto> response = new ArrayList<>();
        for (Summarize summarize : findSummarizes) {
            response.add(UserSummaryResponseDto.builder()
                    .summary(summarize.getSummarize())
                    .categories(summarize.getCategories())
                    .keywords(summarize.getKeywords())
                    .build());
        }

        return response;
    }

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
