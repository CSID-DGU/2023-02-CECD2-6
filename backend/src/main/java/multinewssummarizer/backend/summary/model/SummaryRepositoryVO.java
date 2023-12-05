package multinewssummarizer.backend.summary.model;

import lombok.Getter;
import lombok.ToString;

@Getter
@ToString
public class SummaryRepositoryVO {
    private Long id;
    private String link;
    private String title;
    private String context;

    public SummaryRepositoryVO(Long id, String link, String title, String context) {
        this.id = id;
        this.link = link;
        this.title = title;
        this.context = context;
    }
}
