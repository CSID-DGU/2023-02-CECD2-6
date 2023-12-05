package multinewssummarizer.backend.summary.repository;

import multinewssummarizer.backend.summary.domain.Summarizelog;
import multinewssummarizer.backend.user.domain.Users;
import multinewssummarizer.backend.user.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@SpringBootTest
@Transactional
class SummarizelogRepositoryTest {

    String pattern = "yyyy-MM-dd";
    DateTimeFormatter formatter = DateTimeFormatter.ofPattern(pattern);

    @Autowired
    SummarizelogRepository summarizelogRepository;

    @Autowired
    UserRepository userRepository;

    @BeforeEach
    void beforeEach() {
        summarizelogRepository.deleteAllInBatch();
    }

    @Test
    void add() {
        //given
        Users user = new Users();
        user.setAccountId("temp");
        user.setName("임시");
        user.setPassword("temp1234");
        user.setBirth(LocalDate.parse("2023-12-06", formatter));
        Users savedUser = userRepository.save(user);

        Summarizelog summarizelog = Summarizelog.builder()
                .users(savedUser)
                .summarize("요약")
                .keywords("키워드")
                .categories("카테고리")
                .newsIds("뉴스 id")
                .createdTime(LocalDateTime.now())
                .batchNewsId(null)
                .build();
        Summarizelog savedSummarizeLog = summarizelogRepository.save(summarizelog);
    }
}