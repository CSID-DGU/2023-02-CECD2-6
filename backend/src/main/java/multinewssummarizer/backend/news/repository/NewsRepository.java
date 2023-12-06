package multinewssummarizer.backend.news.repository;

import multinewssummarizer.backend.news.domain.News;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDateTime;
import java.util.List;


public interface NewsRepository extends JpaRepository<News, Long> {

    // 하루 전에 생성된 기사는 가져오는 쿼리문
    @Query(value = "SELECT id FROM News WHERE post_time >= current_timestamp - interval '1 day'", nativeQuery = true)
    List<Long> findNewsByPublishedWithinLastDay();

    @Query(value = "SELECT DISTINCT n FROM News n " +
            "WHERE (:categoryParam IS NOT NULL AND n.topic IN :categoryParam) " +
            "AND n.postTime >= :oneDayAgo " +
            "UNION " +
            "SELECT DISTINCT n FROM News n LEFT JOIN n.keywords k " +
            "WHERE (:keywordParam IS NOT NULL AND k.keyword IN :keywordParam) " +
            "AND n.postTime >= :oneDayAgo")
    List<News> findNewsByCategoriesAndKeywords(
            @Param("categoryParam") List<String> categoriesParam,
            @Param("keywordParam") List<String> keywordsParam,
            @Param("oneDayAgo")LocalDateTime oneDayAgo);
}
