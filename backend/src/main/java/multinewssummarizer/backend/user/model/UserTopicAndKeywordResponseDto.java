package multinewssummarizer.backend.user.model;

import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Getter
@Builder
public class UserTopicAndKeywordResponseDto {
    private List<String> topics;
    private List<String> keywords;
}
