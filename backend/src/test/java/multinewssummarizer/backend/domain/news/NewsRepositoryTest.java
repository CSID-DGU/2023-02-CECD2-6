package multinewssummarizer.backend.domain.news;

import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
@Transactional
class NewsRepositoryTest {

    @Autowired NewsRepository newsRepository;

    @Test
    void testNews() {
        News news = newsRepository.findById(705L).get();

        System.out.println("news = " + news);

        assertThat(news.getId()).isNotNull();
        assertThat(news.getCompanyName()).isNotNull();
        assertThat(news.getLink()).isNotNull();
        assertThat(news.getTitle()).isNotNull();
        assertThat(news.getKeywords()).isNotNull();
        assertThat(news.getTopic()).isNotNull();
    }
}