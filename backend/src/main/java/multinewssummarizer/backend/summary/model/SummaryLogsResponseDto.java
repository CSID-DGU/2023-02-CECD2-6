package multinewssummarizer.backend.summary.model;

import lombok.*;

import java.time.LocalDateTime;
import java.util.List;

@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor(access = AccessLevel.PROTECTED)
public class SummaryLogsResponseDto {
    private String summary;
    private String keywords;
    private String categories;
    private LocalDateTime createdTime;
    private List<SummaryNewsVO> news;
}
