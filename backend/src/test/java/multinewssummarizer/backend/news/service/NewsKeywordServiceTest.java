package multinewssummarizer.backend.news.service;

import multinewssummarizer.backend.news.domain.NewsKeyword;
import multinewssummarizer.backend.news.model.NewsKeywordDTO;
import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
class NewsKeywordServiceTest {

    @Autowired
    NewsKeywordService newsKeywordService;

    @Test
    void findNewsKeywordsByOneId() {
        Long id = 2L;
        List<NewsKeyword> allByNewsId = newsKeywordService.findAllByNewsId(id);

        System.out.println("allByNewsId = " + allByNewsId);

        Assertions.assertThat(allByNewsId).isNotEmpty();
        Assertions.assertThat(allByNewsId.size()).isEqualTo(5);
    }

    @Test
    void findNewsKeywordsByMultipleIds() {
        List<Long> ids = new ArrayList<>(Arrays.asList(2L, 3L, 4L));

        List<NewsKeywordDTO> newsKeywordsByNewsIds = newsKeywordService.findNewsKeywordsByNewsIds(ids);

        System.out.println("newsKeywordsByNewsIds = " + newsKeywordsByNewsIds);

        Assertions.assertThat(newsKeywordsByNewsIds).isNotEmpty();
    }
}