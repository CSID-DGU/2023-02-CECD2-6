package multinewssummarizer.backend.summary.service;

import lombok.RequiredArgsConstructor;
import multinewssummarizer.backend.news.repository.NewsRepository;
import multinewssummarizer.backend.summary.model.SummaryRequestDto;
import multinewssummarizer.backend.summary.model.SummaryResponseDto;
import multinewssummarizer.backend.summary.model.SummaryRepositoryVO;
import multinewssummarizer.backend.user.repository.UserRepository;
import org.json.JSONObject;
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
    private final NewsRepository newsRepository;

    private static String url = "https://dd24-116-255-71-186.ngrok-free.app/summary/";

    @Transactional
    public SummaryResponseDto instantSummary(SummaryRequestDto summaryRequestDto) {
        System.out.println("summaryRequestDto = " + summaryRequestDto);
        ArrayList<String> categories = summaryRequestDto.getCategories();
        ArrayList<String> keywords = summaryRequestDto.getKeywords();
        LocalDateTime oneDayAgo = LocalDateTime.now().minusDays(1);

        List<SummaryRepositoryVO> findNews = newsRepository.findNewsByCategoriesAndKeywords(categories, keywords, oneDayAgo);
        System.out.println("findNews = " + findNews);
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
        String responseBody = rt.postForObject(url, entity, String.class);

        /**TODO:
         * 현재 요약을 한다면, {summary=['더불어민주당이 29일 전날 제출한 이동관 방송통신위원장에 대한 탄핵소추안을 철회한 뒤 다시 제출한다.', ... 민주당은 내년도 예산안 처리를 위해 30일과 다음 달 1일 본회의 일정이 확정돼 있다며 탄핵안을 처리한다는 계획이다.']}
         * 결과로 출력이 된다. 그러나, 이를 VO나 MultiValueMap과 같이 ObjectMapping을 시도한다면, 오류가 발생한다.
         * 아마, 개별적으로 파싱하여 값을 얻는 작업이 필요할 것 같다.
         */

        /**
         * TODO: 만약, 오류가 발생했을 시, postForObject()로 시도한다면 에러세시지가 뜨지 않지만, exchange()로 한다면, <200 OK OK,{summary=}>로 뜬다. exception처리가 필요할수도
         */

        SummaryResponseDto summaryResponseDto = SummaryResponseDto.builder()
                .ids(findIds)
                .links(links)
                .titles(titles)
                .summary(responseBody)
                .build();

        return summaryResponseDto;
    }

    @Transactional
    public SummaryResponseDto testSummary(List<Long> ids) {
        // POST 요청
        RestTemplate rt2 = new RestTemplate();
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        JSONObject body = new JSONObject();
        body.put("numbers", ids);

        HttpEntity<String> entity = new HttpEntity<>(body.toString(), headers);

        try {
//            ResponseEntity<?> responseBody = rt2.exchange(url, HttpMethod.POST, entity, Object.class);
            String responseBody = rt2.postForObject(url, entity, String.class);
            System.out.println("responseBody = " + responseBody);

            SummaryResponseDto summaryResponseDto = SummaryResponseDto.builder()
                    .ids(ids)
                    .links(null)
                    .titles(null)
                    .summary(responseBody.toString())
                    .build();

            return summaryResponseDto;

        } catch (Exception e) {
            throw e;
        }
    }

}
