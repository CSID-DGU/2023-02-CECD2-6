package multinewssummarizer.backend.user.model;

import lombok.*;

import java.time.LocalDate;

@Getter
@Builder
@AllArgsConstructor
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class UserInfoResponseDto {
    private String userId;
    private String name;
    private LocalDate birth;
}
