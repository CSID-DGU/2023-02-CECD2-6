package multinewssummarizer.backend.news.repository;

import multinewssummarizer.backend.summary.model.SummaryRepositoryVO;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

@Transactional
@SpringBootTest
class NewsRepositoryTest {

    @Autowired
    NewsRepository newsRepository;

    @Test
    void categoriesAndKeywords() {
        List<String> categories = new ArrayList<>();
        List<String> keywords = new ArrayList<>();
        LocalDateTime oneDayAgo = LocalDateTime.now().minusDays(1);

        LocalDateTime oneDay = LocalDate.now().minusDays(1).atStartOfDay();
        System.out.println("oneDay = " + oneDay);

        categories.add("정치");
        keywords.add("밥");
        List<SummaryRepositoryVO> output = newsRepository.findNewsByCategoriesAndKeywords(categories, keywords, oneDay);
        System.out.println("output = " + output);
    }
}