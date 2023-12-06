package multinewssummarizer.backend.news.domain;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import multinewssummarizer.backend.news.domain.News;

@Entity
@Table(name = "newskeyword")
@Getter @Setter
public class NewsKeyword {

    @Id @GeneratedValue
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "news_id")
    News news;

    @Column(nullable = false)
    private String keyword;

}
