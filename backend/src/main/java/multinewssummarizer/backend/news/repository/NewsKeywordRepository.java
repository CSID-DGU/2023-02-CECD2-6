package multinewssummarizer.backend.news.repository;

import multinewssummarizer.backend.news.domain.NewsKeyword;
import multinewssummarizer.backend.news.model.NewsKeywordDTO;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;

public interface NewsKeywordRepository extends JpaRepository<NewsKeyword, Long> {
    List<NewsKeyword> findAllByNewsId(Long newsId);

    // 하루 전 뉴스 데이터에 해당하는 id를 통해 뉴스 데이터를 불러오는 쿼리문
    @Query("SELECT new multinewssummarizer.backend.news.model.NewsKeywordDTO(nk.keyword) FROM NewsKeyword nk WHERE nk.news.id IN :ids")
    List<NewsKeywordDTO> findNewsKeywordsByNewsIds(List<Long> ids);
}
