package multinewssummarizer.backend.summary.repository;

import multinewssummarizer.backend.summary.domain.Summarize;
import multinewssummarizer.backend.user.domain.Users;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface SummarizeRepository extends JpaRepository<Summarize, Long> {

    List<Summarize> findByUsers(Users findUser);

}
