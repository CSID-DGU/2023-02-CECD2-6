package multinewssummarizer.backend.user.controller;

import lombok.RequiredArgsConstructor;
import multinewssummarizer.backend.user.model.UserTopicAndKeywordRequestDto;
import multinewssummarizer.backend.user.model.UserTopicAndKeywordResponseDto;
import multinewssummarizer.backend.user.service.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/user")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @PostMapping("/register")
    public ResponseEntity<String> registerTopicsAndKeywords(@RequestBody UserTopicAndKeywordRequestDto userTopicAndKeywordRequestDto) {
        Long userId = userService.registerTopicsAndKeywords(userTopicAndKeywordRequestDto);
        return ResponseEntity.ok("OK");
    }

    @GetMapping("/topicsandkeywords")
    public ResponseEntity<UserTopicAndKeywordResponseDto> getTopicsAndKeywords(@RequestParam("id") Long userId) {
        UserTopicAndKeywordResponseDto topicsAndKeywords = userService.getTopicsAndKeywords(userId);
        return ResponseEntity.ok(topicsAndKeywords);
    }
}
