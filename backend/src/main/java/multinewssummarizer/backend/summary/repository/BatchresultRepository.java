package multinewssummarizer.backend.summary.repository;

import multinewssummarizer.backend.summary.domain.Batchresult;
import org.springframework.data.jpa.repository.JpaRepository;

public interface BatchresultRepository extends JpaRepository<Batchresult, Long> {
}
