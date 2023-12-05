package multinewssummarizer.backend.summary.repository;

import multinewssummarizer.backend.summary.domain.SummarizeLog;
import multinewssummarizer.backend.user.domain.Users;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface SummarizeRepository extends JpaRepository<SummarizeLog, Long> {

    List<SummarizeLog> findByUsers(Users findUser);

}
