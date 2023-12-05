package multinewssummarizer.backend.user.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;

@Getter
@AllArgsConstructor
@Builder
public class UserSignInResponseDto {
    private Long userId;
    private String name;
    private Boolean keywords;
    private Boolean categories;
}