package multinewssummarizer.backend.user.model;

import lombok.*;

import java.beans.ConstructorProperties;

@Getter
@Builder
@ToString
public class UserSignInRequestDto {
    private String accountId;
    private String password;

    @ConstructorProperties({"accountId", "password"})
    public UserSignInRequestDto(String accountId, String password) {
        this.accountId = accountId;
        this.password = password;
    }
}
