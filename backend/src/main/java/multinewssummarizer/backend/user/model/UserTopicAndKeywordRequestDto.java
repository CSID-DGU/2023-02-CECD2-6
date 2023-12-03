package multinewssummarizer.backend.user.model;

import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter @Setter
public class UserTopicAndKeywordRequestDto {
    private Long userId;
    private List<String> topics;
    private List<String> keywords;
}
