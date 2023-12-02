package multinewssummarizer.backend.summary.model;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.util.ArrayList;

@Getter @Setter
@ToString
public class SummaryRequestDto {
    private Long userId;
    private ArrayList<String> categories;
    private ArrayList<String> keywords;
}
