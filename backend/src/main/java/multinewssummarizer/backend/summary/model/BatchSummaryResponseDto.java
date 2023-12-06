package multinewssummarizer.backend.summary.model;

import lombok.*;

import java.util.List;

@Getter
@Builder
@AllArgsConstructor(access = AccessLevel.PROTECTED)
@NoArgsConstructor
public class BatchSummaryResponseDto {
    private List<String> summary;
    private List<SummaryNewsVO> news;
}
