package multinewssummarizer.backend.summary.model;

import lombok.*;

@Builder
@Getter
@NoArgsConstructor
@AllArgsConstructor(access = AccessLevel.PROTECTED)
public class UserSummaryResponseDto {
    private String summary;
    private String categories;
    private String keywords;
}
