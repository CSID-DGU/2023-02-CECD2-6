package multinewssummarizer.backend.summary.model;

import lombok.*;

@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor(access = AccessLevel.PROTECTED)
public class SummaryNewsVO {
    private String title;
    private String context;
    private String companyName;
    private String link;
}
