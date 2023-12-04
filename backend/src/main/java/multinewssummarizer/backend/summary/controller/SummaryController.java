package multinewssummarizer.backend.summary.controller;

import lombok.RequiredArgsConstructor;
import multinewssummarizer.backend.global.exceptionhandler.CustomExceptions;
import multinewssummarizer.backend.summary.model.SummaryRequestDto;
import multinewssummarizer.backend.summary.model.SummaryResponseDto;
import multinewssummarizer.backend.summary.service.SummaryService;
import multinewssummarizer.backend.summary.model.UserSummaryResponseDto;
import org.json.simple.parser.ParseException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/summary")
@RequiredArgsConstructor
public class SummaryController {

    private final SummaryService summaryService;

    @PostMapping("/instant")
    public ResponseEntity<SummaryResponseDto> instantSummary(@RequestBody SummaryRequestDto summaryRequestDto) throws ParseException{
        SummaryResponseDto news = summaryService.instantSummary(summaryRequestDto);
        return new ResponseEntity<>(news, HttpStatus.OK);
    }

    @ExceptionHandler(CustomExceptions.NoNewsDataException.class)
    public ResponseEntity<String> handleNoNewsException(CustomExceptions.NoNewsDataException ex) {
        return new ResponseEntity<>(ex.getMessage(), HttpStatus.BAD_REQUEST);
    }

    @GetMapping("/getusersummary")
    public ResponseEntity<List<UserSummaryResponseDto>> getSummarizeLogs(@RequestParam("id") Long userId) {
        List<UserSummaryResponseDto> response = summaryService.getUserSummaryLogs(userId);
        return ResponseEntity.ok(response);
    }
}
