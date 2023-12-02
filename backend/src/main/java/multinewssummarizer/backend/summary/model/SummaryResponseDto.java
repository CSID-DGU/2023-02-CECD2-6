package multinewssummarizer.backend.summary.model;

import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Builder
public class SummaryResponseDto {
    private List<Long> ids;
    private List<String> links;
    private List<String> titles;
    private String summary;
}
