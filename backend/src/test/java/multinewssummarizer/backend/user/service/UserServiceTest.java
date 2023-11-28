package multinewssummarizer.backend.user.service;

import multinewssummarizer.backend.user.domain.Users;
import multinewssummarizer.backend.user.model.UserSignInRequestDto;
import multinewssummarizer.backend.user.model.UserSignUpRequestDto;
import multinewssummarizer.backend.user.repository.UserRepository;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.transaction.annotation.Transactional;

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

    @BeforeEach
    void beforeEach() {userRepository.deleteAllInBatch();}

    @Test
    @Transactional
    void wrongRegister() throws Exception{
        //given
        UserSignUpRequestDto temp = new UserSignUpRequestDto("temp", "임시", "temp12", "temp12");
        userService.signUp(temp);

        UserSignUpRequestDto duplicatedUser = new UserSignUpRequestDto("temp", "임시2", "temp123", "temp123");
        UserSignUpRequestDto incorrectPasswordUser = new UserSignUpRequestDto("temp2", "임시2", "temp12", "temp123");

        Assertions.assertThrows(Exception.class, () ->
                userService.signUp(duplicatedUser));

        Assertions.assertThrows(Exception.class, () ->
                userService.signUp(incorrectPasswordUser));
    }

    @Test
    @Transactional
    void correctRegister() throws Exception{
        //given
        UserSignUpRequestDto user = new UserSignUpRequestDto("temp", "임시", "temp12", "temp12");
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
        UserSignUpRequestDto user = new UserSignUpRequestDto("temp", "임시", "temp12", "temp12");
        userService.signUp(user);

        UserSignInRequestDto request1 = new UserSignInRequestDto("wrong", "temp12");
        UserSignInRequestDto request2 = new UserSignInRequestDto("temp", "wrong");
        Assertions.assertThrows(IllegalArgumentException.class, () ->
                userService.signIn(request1));

        Assertions.assertThrows(IllegalArgumentException.class, () ->
                userService.signIn(request2));
    }

    @Test
    @Transactional
    void correctSignIn() throws Exception{
        //given
        UserSignUpRequestDto user = new UserSignUpRequestDto("temp", "임시", "temp12", "temp12");
        userService.signUp(user);

        UserSignInRequestDto request = new UserSignInRequestDto("temp", "temp12");
        Long userId = userService.signIn(request);
        assertThat(userId).isNotNull();

        Optional<Users> out = userRepository.findById(userId);
        Users findUser = out.get();

        assertThat(findUser.getAccountId()).isEqualTo(request.getAccountId());
        assertThat(passwordEncoder.matches(request.getPassword(), findUser.getPassword())).isTrue();
    }
}