package multinewssummarizer.backend.news.service;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
class NewsServiceTest {

    @Autowired
    NewsService newsService;

//    @Test
//    void findNewsIdsWithinOneDay() {
//        List<Long> newsIdsWithinLastDay = newsService.getNewsIdsWithinLastDay();
//
//        System.out.println("newsIdsWithinLastDay = " + newsIdsWithinLastDay);
//
//        assertThat(newsIdsWithinLastDay).isNotEmpty();
//    }
}