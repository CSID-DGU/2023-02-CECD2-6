package multinewssummarizer.backend.summary.controller;

import lombok.RequiredArgsConstructor;
import multinewssummarizer.backend.summary.model.SummaryRequestDto;
import multinewssummarizer.backend.summary.model.SummaryResponseDto;
import multinewssummarizer.backend.summary.service.SummaryService;
import multinewssummarizer.backend.user.service.UserService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/summary")
@RequiredArgsConstructor
public class SummaryController {

    private final UserService userService;
    private final SummaryService summaryService;

    @PostMapping("/instant")
    public ResponseEntity<SummaryResponseDto> instantSummary(@RequestBody SummaryRequestDto summaryRequestDto) {
        SummaryResponseDto news = summaryService.instantSummary(summaryRequestDto);
        return new ResponseEntity<>(news, HttpStatus.OK);
    }

    @PostMapping("/test")
    public ResponseEntity<SummaryResponseDto> testSummary(@RequestBody List<Long> ids) {
        SummaryResponseDto news = summaryService.testSummary(ids);
        return new ResponseEntity<>(news, HttpStatus.OK);
    }
}
