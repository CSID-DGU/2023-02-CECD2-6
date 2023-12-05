package multinewssummarizer.backend.summary.repository;

import multinewssummarizer.backend.summary.domain.Summarizelog;
import multinewssummarizer.backend.user.domain.Users;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface SummarizelogRepository extends JpaRepository<Summarizelog, Long> {

    List<Summarizelog> findByUsers(Users findUser);

    @Query(value = "SELECT s FROM Summarizelog s WHERE s.batchNewsId = :batchNewsId")
    Optional<Summarizelog> findByBatchnewsId(@Param("batchNewsId") Long batchNewsId);
}
