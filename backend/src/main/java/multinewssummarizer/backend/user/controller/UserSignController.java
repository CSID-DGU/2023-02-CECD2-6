package multinewssummarizer.backend.user.controller;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import multinewssummarizer.backend.global.exceptionhandler.CustomExceptions;
import multinewssummarizer.backend.user.model.UserSignInRequestDto;
import multinewssummarizer.backend.user.model.UserSignUpRequestDto;
import multinewssummarizer.backend.user.service.UserService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.*;


@RestController
@RequestMapping("/user")
@RequiredArgsConstructor
public class UserSignController {

    private final UserService userService;

    @PostMapping("/sign-up")
    public ResponseEntity<Long> signUp(@Valid @ModelAttribute UserSignUpRequestDto user) throws Exception {
        Long userId = userService.signUp(user);
        return ResponseEntity.ok(userId);
    }

    @ExceptionHandler(CustomExceptions.ExistingIdException.class)
    public ResponseEntity<String> handleExistingId(CustomExceptions.ExistingIdException ex) {
        return new ResponseEntity<>(ex.getMessage(), HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(CustomExceptions.WrongPasswordException.class)
    public ResponseEntity<String> handleWrongPassword(CustomExceptions.WrongPasswordException ex) {
        return new ResponseEntity<>(ex.getMessage(), HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<String> handleValidationException(MethodArgumentNotValidException ex) {
        return new ResponseEntity<>(ex.getMessage(), HttpStatus.BAD_REQUEST);
    }

    @PostMapping("/sign-in")
    public ResponseEntity<Long> signIn(@ModelAttribute UserSignInRequestDto request) throws Exception {
        Long userId = userService.signIn(request);
        return ResponseEntity.ok(userId);
    }

    @ExceptionHandler(CustomExceptions.IllegalArgumentLoginException.class)
    public ResponseEntity<String> handleIllegalArgumentLoginException(CustomExceptions.IllegalArgumentLoginException ex) {
        return new ResponseEntity<>(ex.getMessage(), HttpStatus.BAD_REQUEST);
    }
}
