package multinewssummarizer.backend.user.service;

import lombok.RequiredArgsConstructor;
import multinewssummarizer.backend.global.exceptionhandler.CustomExceptions;
import multinewssummarizer.backend.summary.domain.Summarize;
import multinewssummarizer.backend.user.domain.Users;
import multinewssummarizer.backend.user.model.*;
import multinewssummarizer.backend.user.repository.UserRepository;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    @Transactional
    public Long signUp(UserSignUpRequestDto requestDto) {

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
    public UserSignInResponseDto signIn(UserSignInRequestDto requestDto) throws Exception {
        Users findUser = userRepository.findByAccountId(requestDto.getAccountId())
                .orElseThrow(() -> new CustomExceptions.IllegalArgumentLoginException("아이디 또는 비밀번호가 일치하지 않습니다."));

        if(!passwordEncoder.matches(requestDto.getPassword(), findUser.getPassword())) {
            throw new CustomExceptions.IllegalArgumentLoginException("아이디 또는 비밀번호가 일치하지 않습니다.");
        }

        boolean keywords = false;
        boolean categories = false;

        if(findUser.getTopics() != null) {
            categories = true;
        }
        if(findUser.getKeywords() != null) {
            keywords = true;
        }

        UserSignInResponseDto userSignInResponseDto = UserSignInResponseDto.builder()
                .userId(findUser.getId())
                .categories(categories)
                .keywords(keywords)
                .build();
        return userSignInResponseDto;
    }

    @Transactional
    public Long registerTopicsAndKeywords(UserTopicAndKeywordRequestDto userTopicAndKeywordRequestDto) {
        System.out.println("userTopicAndKeywordRequestDto = " + userTopicAndKeywordRequestDto);
        Users user = userRepository.findById(userTopicAndKeywordRequestDto.getUserId()).orElseThrow();

        if (!userTopicAndKeywordRequestDto.getKeywords().isEmpty()) {
            String keywords = "";
            for (String keyword: userTopicAndKeywordRequestDto.getKeywords()) {
                keywords += keyword;
                keywords += ",";
            }
            keywords = keywords.substring(0, keywords.length() - 1);
            user.setKeywords(keywords);
        } else {
            user.setKeywords(null);
        }
        if (!userTopicAndKeywordRequestDto.getTopics().isEmpty()) {
            String topics = "";
            for (String topic: userTopicAndKeywordRequestDto.getTopics()) {
                topics += topic;
                topics += ",";
            }
            topics = topics.substring(0, topics.length() - 1);
            user.setTopics(topics);
        } else {
            user.setTopics(null);
        }

        Users savedUser = userRepository.save(user);
        return savedUser.getId();
    }

    @Transactional
    public UserTopicAndKeywordResponseDto getTopicsAndKeywords(Long userId) {
        Users findUser = userRepository.findById(userId).orElseThrow();

        List<String> keywords = new ArrayList<>();
        List<String> topics = new ArrayList<>();

        if(findUser.getKeywords() != null) {
            String rawKeywords = findUser.getKeywords();
            String[] splitKeywords = rawKeywords.split(",");

            for (String splitKeyword : splitKeywords) {
                keywords.add(splitKeyword);
            }
        }
        if(findUser.getTopics() != null) {
            String rawTopics = findUser.getTopics();
            String[] splitTopics = rawTopics.split(",");

            for (String splitTopic : splitTopics) {
                topics.add(splitTopic);
            }
        }

        UserTopicAndKeywordResponseDto res = UserTopicAndKeywordResponseDto.builder()
                .topics(topics)
                .keywords(keywords)
                .build();

        return res;
    }


}
