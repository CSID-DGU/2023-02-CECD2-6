package multinewssummarizer.backend.news.domain;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.time.LocalDateTime;
import java.util.List;

@Entity
@Getter @Setter
public class News {

    @Id @GeneratedValue
    private Long id;

    @Column(nullable = false)
    private String companyName;

    @Column(nullable = false)
    private String topic;

    @Column(nullable = false)
    private String title;

    @Column(nullable = false)
    private String link;

    @Column(nullable = false)
    private String context;

    @Column(nullable = false)
    private LocalDateTime postTime;

    @OneToMany(mappedBy = "news", cascade = CascadeType.ALL)
    private List<NewsKeyword> keywords;
}
