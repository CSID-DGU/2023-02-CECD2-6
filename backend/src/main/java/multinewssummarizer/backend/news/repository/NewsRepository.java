package multinewssummarizer.backend.news.repository;

import multinewssummarizer.backend.news.domain.News;
import multinewssummarizer.backend.summary.model.SummaryRepositoryVO;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDateTime;
import java.util.List;


public interface NewsRepository extends JpaRepository<News, Long> {

    // 하루 전에 생성된 기사는 가져오는 쿼리문
    @Query(value = "SELECT id FROM News WHERE post_time >= current_timestamp - interval '1 day'", nativeQuery = true)
    List<Long> findNewsByPublishedWithinLastDay();

    @Query(value = "SELECT DISTINCT new multinewssummarizer.backend.summary.model.SummaryRepositoryVO(n.id, n.link, n.title) FROM News n LEFT JOIN n.keywords k " +
            "WHERE ((:categoryParam IS NULL OR n.topic IN :categoryParam) " +
            "OR (:keywordParam IS NULL OR k.keyword IN :keywordParam)) " +
            "AND n.postTime >= :oneDayAgo")
    List<SummaryRepositoryVO> findNewsByCategoriesAndKeywords(
            @Param("categoryParam") List<String> categoriesParam,
            @Param("keywordParam") List<String> keywordsParam,
            @Param("oneDayAgo")LocalDateTime oneDayAgo);
}
