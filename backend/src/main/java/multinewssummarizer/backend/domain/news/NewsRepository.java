package multinewssummarizer.backend.domain.news;

import org.springframework.data.jpa.repository.JpaRepository;


public interface NewsRepository extends JpaRepository<News, Long> {
}
