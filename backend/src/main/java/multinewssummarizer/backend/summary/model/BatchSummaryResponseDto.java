package multinewssummarizer.backend.summary.model;

import lombok.*;

import java.util.List;

@Getter
@Builder
@AllArgsConstructor(access = AccessLevel.PROTECTED)
@NoArgsConstructor
public class BatchSummaryResponseDto {
    private String summary;
    private List<BatchSummaryNewsVO> news;
}
