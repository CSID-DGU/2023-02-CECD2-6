package multinewssummarizer.backend.summary.domain;

import jakarta.persistence.*;
import lombok.*;
import multinewssummarizer.backend.user.domain.Users;

@Entity
@Getter
@NoArgsConstructor
public class Summarize {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    Users users;

    @Column(nullable = false)
    private String summarize;

    @Column
    private String categories;

    @Column
    private String keywords;

    @Builder
    public Summarize (Users users, String summarize, String categories, String keywords) {
        this.users = users;
        this.summarize = summarize;
        this.categories = categories;
        this.keywords = keywords;
    }
}
