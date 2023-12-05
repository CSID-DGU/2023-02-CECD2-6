package multinewssummarizer.backend.summary.controller;

import lombok.RequiredArgsConstructor;
import multinewssummarizer.backend.global.exceptionhandler.CustomExceptions;
import multinewssummarizer.backend.summary.model.*;
import multinewssummarizer.backend.summary.service.SummaryService;
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
    public ResponseEntity<List<SummaryLogsResponseDto>> getSummarizeLogs(@RequestParam("id") Long userId) {
        List<SummaryLogsResponseDto> response = summaryService.getUserSummaryLogs(userId);
        return ResponseEntity.ok(response);
    }

    @ExceptionHandler(CustomExceptions.NoSummaryLogException.class)
    public ResponseEntity<String> handleNoSummaryLogsException(CustomExceptions.NoSummaryLogException ex) {
        return new ResponseEntity<>(ex.getMessage(), HttpStatus.BAD_REQUEST);
    }

    @GetMapping("/rsscomplete")
    public ResponseEntity<Boolean> batchSummary() throws ParseException {
        boolean response = summaryService.batchSummary();
        return ResponseEntity.ok(response);
    }

    @GetMapping("/getlastbatchsummary")
    public ResponseEntity<BatchSummaryResponseDto> getLastBatchSummary(@RequestParam("id") Long userId) {
        BatchSummaryResponseDto lastBatchSummary = summaryService.getLastBatchSummary(userId);
        return ResponseEntity.ok(lastBatchSummary);
    }

    @ExceptionHandler(CustomExceptions.NoBatchNewsDataException.class)
    public ResponseEntity<String> handleNoBatchNewsDataException(CustomExceptions.NoBatchNewsDataException ex) {
        return new ResponseEntity<>(ex.getMessage(), HttpStatus.BAD_REQUEST);
    }
}
