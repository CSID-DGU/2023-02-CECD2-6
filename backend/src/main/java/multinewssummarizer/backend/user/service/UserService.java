package multinewssummarizer.backend.user.service;

import lombok.RequiredArgsConstructor;
import multinewssummarizer.backend.global.exceptionhandler.CustomExceptions;
import multinewssummarizer.backend.user.domain.Users;
import multinewssummarizer.backend.user.model.UserSignInRequestDto;
import multinewssummarizer.backend.user.model.UserSignUpRequestDto;
import multinewssummarizer.backend.user.repository.UserRepository;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    @Transactional
    public Long signUp(UserSignUpRequestDto requestDto) throws Exception{

        if(userRepository.findByAccountId(requestDto.getAccountId()).isPresent()) {
            throw new CustomExceptions.ExistingIdException("이미 존재하는 아이디 입니다.");
        }
        if(!requestDto.getPassword().equals(requestDto.getCheckedPassword())) {
            throw new CustomExceptions.WrongPasswordException("비밀번호가 일치하지 않습니다.");
        }

        Users savedUser = userRepository.save(requestDto.toEntity());
        savedUser.encodePassword(passwordEncoder);

        return savedUser.getId();
    }

    @Transactional
    public Long signIn(UserSignInRequestDto requestDto) throws Exception {
        Users findUser = userRepository.findByAccountId(requestDto.getAccountId())
                .orElseThrow(() -> new CustomExceptions.IllegalArgumentLoginException("아이디 또는 비밀번호가 일치하지 않습니다."));

        if(!passwordEncoder.matches(requestDto.getPassword(), findUser.getPassword())) {
            throw new CustomExceptions.IllegalArgumentLoginException("아이디 또는 비밀번호가 일치하지 않습니다.");
        }

        return findUser.getId();
    }
}
