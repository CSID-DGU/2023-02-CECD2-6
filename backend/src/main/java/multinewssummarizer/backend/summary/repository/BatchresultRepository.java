package multinewssummarizer.backend.summary.repository;

import multinewssummarizer.backend.summary.domain.Batchresult;
import multinewssummarizer.backend.user.domain.Users;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.Optional;

public interface BatchresultRepository extends JpaRepository<Batchresult, Long> {
    @Query(value = "SELECT b FROM Batchresult b WHERE b.users = :user ORDER BY b.id DESC LIMIT 1")
    Optional<Batchresult> findLastSummaryByUserId(@Param("user") Users user);
}
