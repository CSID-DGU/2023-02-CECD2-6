package multinewssummarizer.backend.summary.model;

import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Builder
public class SummaryResponseDto {
    private List<String> summary;
    private List<SummaryNewsVO> news;
}
