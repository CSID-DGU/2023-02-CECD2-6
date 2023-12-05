package multinewssummarizer.backend.summary.domain;

import jakarta.persistence.*;
import lombok.*;
import multinewssummarizer.backend.user.domain.Users;

import java.time.LocalDateTime;

@Entity
@Table(name = "SummarizeLog")
@Getter
@Builder
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor
public class SummarizeLog {
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

    @Column(nullable = false)
    private String newsIds;

    @Column(nullable = false)
    private LocalDateTime createdTime;

    @Column(name = "batchnews_id")
    private Long batchNewsId;

}
