package multinewssummarizer.backend.user.service;

import multinewssummarizer.backend.global.exceptionhandler.CustomExceptions;
import multinewssummarizer.backend.user.domain.Users;
import multinewssummarizer.backend.user.model.UserSignInRequestDto;
import multinewssummarizer.backend.user.model.UserSignInResponseDto;
import multinewssummarizer.backend.user.model.UserSignUpRequestDto;
import multinewssummarizer.backend.user.repository.UserRepository;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
class UserServiceTest {

    @Autowired
    UserService userService;

    @Autowired
    UserRepository userRepository;

    @Autowired
    PasswordEncoder passwordEncoder;

    String pattern = "yyyy-MM-dd";
    DateTimeFormatter formatter = DateTimeFormatter.ofPattern(pattern);

    @BeforeEach
    void beforeEach() {userRepository.deleteAllInBatch();}

    @Test
    @Transactional
    void wrongRegister() throws Exception{
        //given
        UserSignUpRequestDto temp = new UserSignUpRequestDto();
        temp.setAccountId("temp");
        temp.setName("임시");
        temp.setPassword("temp12");
        temp.setCheckedPassword("temp12");
        temp.setBirth(LocalDate.parse("2023-11-29", formatter));

        userService.signUp(temp);

        UserSignUpRequestDto duplicatedUser = new UserSignUpRequestDto();
        duplicatedUser.setAccountId("temp");
        duplicatedUser.setName("임시2");
        duplicatedUser.setPassword("temp123");
        duplicatedUser.setCheckedPassword("temp123");
        duplicatedUser.setBirth(LocalDate.parse("2023-11-29", formatter));

        UserSignUpRequestDto incorrectPasswordUser = new UserSignUpRequestDto();
        incorrectPasswordUser.setAccountId("temp2");
        incorrectPasswordUser.setName("임시2");
        incorrectPasswordUser.setPassword("temp12");
        incorrectPasswordUser.setCheckedPassword("temp123");
        incorrectPasswordUser.setBirth(LocalDate.parse("2023-11-29", formatter));

        Assertions.assertThrows(Exception.class, () ->
                userService.signUp(duplicatedUser));

        Assertions.assertThrows(Exception.class, () ->
                userService.signUp(incorrectPasswordUser));
    }

    @Test
    @Transactional
    void correctRegister() throws Exception{
        //given
        UserSignUpRequestDto user = new UserSignUpRequestDto();
        user.setAccountId("temp");
        user.setName("임시");
        user.setPassword("temp12");
        user.setCheckedPassword("temp12");
        user.setBirth(LocalDate.parse("2023-11-29", formatter));
        Long userId = userService.signUp(user);

        Optional<Users> out = userRepository.findById(userId);
        Users findUser = out.get();
        assertThat(findUser).isNotNull();
        assertThat(findUser.getAccountId()).isEqualTo(user.getAccountId());
        assertThat(findUser.getName()).isEqualTo(user.getName());
        assertThat(passwordEncoder.matches(user.getPassword(), findUser.getPassword())).isTrue();
    }

    @Test
    @Transactional
    void wrongSignIn() throws Exception{
        //given
        UserSignUpRequestDto user = new UserSignUpRequestDto();
        user.setAccountId("temp");
        user.setName("임시");
        user.setPassword("temp12");
        user.setCheckedPassword("temp12");
        user.setBirth(LocalDate.parse("2023-11-29", formatter));
        userService.signUp(user);

        UserSignInRequestDto request1 = new UserSignInRequestDto("wrong", "temp12");
        UserSignInRequestDto request2 = new UserSignInRequestDto("temp", "wrong");
        Assertions.assertThrows(CustomExceptions.IllegalArgumentLoginException.class, () ->
                userService.signIn(request1));

        Assertions.assertThrows(CustomExceptions.IllegalArgumentLoginException.class, () ->
                userService.signIn(request2));
    }

    @Test
    @Transactional
    void correctSignIn() throws Exception{
        //given
        UserSignUpRequestDto user = new UserSignUpRequestDto();
        user.setAccountId("temp");
        user.setName("임시");
        user.setPassword("temp12");
        user.setCheckedPassword("temp12");
        user.setBirth(LocalDate.parse("2023-11-29", formatter));
        userService.signUp(user);

        UserSignInRequestDto request = new UserSignInRequestDto("temp", "temp12");
        UserSignInResponseDto userSignInResponseDto = userService.signIn(request);
        assertThat(userSignInResponseDto).isNotNull();

        Optional<Users> out = userRepository.findById(userSignInResponseDto.getUserId());
        Users findUser = out.get();

        assertThat(findUser.getAccountId()).isEqualTo(request.getAccountId());
        assertThat(passwordEncoder.matches(request.getPassword(), findUser.getPassword())).isTrue();
    }
}