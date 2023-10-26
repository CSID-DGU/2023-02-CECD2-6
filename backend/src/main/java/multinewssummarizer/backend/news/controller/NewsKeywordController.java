package multinewssummarizer.backend.news.controller;

import lombok.RequiredArgsConstructor;
import multinewssummarizer.backend.news.model.NewsKeywordDTO;
import multinewssummarizer.backend.news.service.NewsKeywordComplexService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@RestController
@RequiredArgsConstructor
public class NewsKeywordController {

    @Autowired
    private NewsKeywordComplexService newsKeywordComplexService;

    @GetMapping("/getKeywords")
    public Map<String, Integer> getKeywords() {
        Map<String, Integer> keywordsWithinOneDay = new ConcurrentHashMap<>();

        List<NewsKeywordDTO> keywordsWithinDay = newsKeywordComplexService.findKeywordsWithinDay();

        for (NewsKeywordDTO keywordDTO : keywordsWithinDay) {
            String keyword = keywordDTO.getKeyword();
            keywordsWithinOneDay.put(keyword, keywordsWithinOneDay.getOrDefault(keyword, 0) + 1);
        }

        return keywordsWithinOneDay;
    }
}
