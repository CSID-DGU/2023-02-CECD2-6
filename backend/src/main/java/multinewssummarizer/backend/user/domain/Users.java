package multinewssummarizer.backend.user.domain;

import jakarta.persistence.*;
import lombok.*;
import multinewssummarizer.backend.summary.domain.Summarize;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.time.LocalDate;
import java.util.List;

@Entity
@Getter @Setter
@Builder
@ToString
@AllArgsConstructor
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Users {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "account_id", nullable = false)
    private String accountId;

    @Column(nullable = false)
    private String password;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private LocalDate birth;

    @Column
    private String topics;

    @Column
    private String keywords;

    @OneToMany(mappedBy = "summarize", cascade = CascadeType.ALL)
    private List<Summarize> summarizes;

    public void encodePassword(PasswordEncoder passwordEncoder) {
        this.password = passwordEncoder.encode(password);
    }

}
