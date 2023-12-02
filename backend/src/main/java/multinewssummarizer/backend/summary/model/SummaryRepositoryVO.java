package multinewssummarizer.backend.summary.model;

import lombok.Getter;
import lombok.ToString;

@Getter
@ToString
public class SummaryRepositoryVO {
    private Long id;
    private String link;
    private String title;

    public SummaryRepositoryVO(Long id, String link, String title) {
        this.id = id;
        this.link = link;
        this.title = title;
    }
}
