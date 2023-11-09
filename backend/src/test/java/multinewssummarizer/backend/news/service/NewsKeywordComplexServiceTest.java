package multinewssummarizer.backend.news.service;

import multinewssummarizer.backend.news.model.NewsKeywordDTO;
import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
class NewsKeywordComplexServiceTest {

    @Autowired
    NewsKeywordComplexService newsKeywordComplexService;

//    @Test
//    void findNewsKeywordsWithinOneDay() {
//        List<NewsKeywordDTO> keywordsWithinDay = newsKeywordComplexService.findKeywordsWithinDay();
//
//        System.out.println("keywordsWithinDay = " + keywordsWithinDay);
//
////        Assertions.assertThat(keywordsWithinDay).isNotEmpty();
//    }
}