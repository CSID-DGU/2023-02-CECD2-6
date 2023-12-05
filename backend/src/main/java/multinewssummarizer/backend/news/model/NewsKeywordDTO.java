package multinewssummarizer.backend.news.model;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter @Setter
@ToString
public class NewsKeywordDTO {
    private String keyword;

    public NewsKeywordDTO(String keyword) {
        this.keyword = keyword;
    }
}
