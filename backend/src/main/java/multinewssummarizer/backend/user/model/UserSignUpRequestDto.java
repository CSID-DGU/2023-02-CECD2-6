package multinewssummarizer.backend.user.model;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import multinewssummarizer.backend.user.domain.Users;

@Data
@Builder
@AllArgsConstructor
public class UserSignUpRequestDto {

    @NotBlank(message = "아이디를 입력해 주세요")
    private String accountId;

    @NotBlank(message = "이름을 입력해 주세요")
    private String name;

    @NotBlank(message = "비밀번호를 입력해 주세요")
    @Pattern(regexp = "^(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d]{8,30}$",
            message = "비밀번호는 8~30 자리이면서 1개 이상의 알파벳, 숫자를 포함해야합니다.")
    private String password;

    private String checkedPassword;

    @Builder
    public Users toEntity() {
        return Users.builder()
                .accountId(accountId)
                .name(name)
                .password(password)
                .build();
    }
}
