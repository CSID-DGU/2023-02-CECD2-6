package multinewssummarizer.backend.summary.repository;

import multinewssummarizer.backend.summary.domain.BatchResult;
import org.springframework.data.jpa.repository.JpaRepository;

public interface BatchResultRepository extends JpaRepository<BatchResult, Long> {
}
