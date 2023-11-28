package multinewssummarizer.backend.user.model;

import lombok.*;

@Getter
@AllArgsConstructor
@Builder
@ToString
public class UserSignInRequestDto {
    private String accountId;
    private String password;
}
