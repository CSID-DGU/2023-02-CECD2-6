package multinewssummarizer.backend.news.service;

import multinewssummarizer.backend.news.domain.NewsKeyword;
import multinewssummarizer.backend.news.model.NewsKeywordDTO;
import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
@Transactional(readOnly = true)
class NewsKeywordServiceTest {

    @Autowired
    NewsKeywordService newsKeywordService;

    @Test
    void findNewsKeywordsByMultipleIds() {
        List<Long> ids = new ArrayList<>(Arrays.asList(2L, 3L, 4L));

        List<NewsKeywordDTO> newsKeywordsByNewsIds = newsKeywordService.findNewsKeywordsByNewsIds(ids);

        System.out.println("newsKeywordsByNewsIds = " + newsKeywordsByNewsIds);

//        Assertions.assertThat(newsKeywordsByNewsIds).isNotEmpty();
    }
}