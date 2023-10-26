package multinewssummarizer.backend.news.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.time.LocalDateTime;

@Entity
@Getter @Setter
@ToString
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
}
