package multinewssummarizer.backend.summary.repository;

import multinewssummarizer.backend.summary.domain.Summarizelog;
import multinewssummarizer.backend.user.domain.Users;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface SummarizelogRepository extends JpaRepository<Summarizelog, Long> {

    List<Summarizelog> findByUsers(Users findUser);

}
