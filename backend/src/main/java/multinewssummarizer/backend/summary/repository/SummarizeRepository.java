package multinewssummarizer.backend.summary.repository;

import multinewssummarizer.backend.summary.domain.Summarize;
import org.springframework.data.jpa.repository.JpaRepository;

public interface SummarizeRepository extends JpaRepository<Summarize, Long> {
}
