package multinewssummarizer.backend.news.repository;

import multinewssummarizer.backend.news.domain.News;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;


public interface NewsRepository extends JpaRepository<News, Long> {

    // 하루 전에 생성된 기사는 가져오는 쿼리문
    @Query(value = "SELECT id FROM News WHERE post_time >= current_timestamp - interval '1 day'", nativeQuery = true)
    List<Long> findNewsByPublishedWithinLastDay();
}
