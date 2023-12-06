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
import java.util.ArrayList;
import java.util.List;
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

    @Test
    void dummy() {
        String dummy = "그래놓고는 이 채용에 응시해 경영기획팀장으로 최종 합격했다. 이 축구단 사무국장이었던 a씨는 지난해 경영기획팀장을 채용한다는 계획을 세우고, 인사위원회 개최와 채용 공고 등을 결재권자로서 직접 진행했다. 539곳은 최근 3년 내에 채용 관련 조사를 받았으나 채용 비리가 포착되지 않아, 이번 조사에서 제외됐다. 경영기획팀장은 사무국장의 부하 직원이지만, 사무국장은 2년 단위 계약직인 반면 팀장은 상근직이었다. 이를 포함해 공공기관 임직원 68명이 채용 비리에 연루됐고, 이로 인해 최소 14명이 중간 합격 또는 최종 합격할 채용에서 부당하게 탈락하는 피해를 입었다. 그러자 단장은 채점 위원 3명 가운데 1명이 매긴 점수를 빼고 나머지 2명이 매긴 점수만으로 점수를 다시 계산하게 해 지인을 합격시켰다. 공공기관 825곳이 지난해 진행한 채용을 정부가 전수 조사한 결과, 절반이 넘는 454곳(55%)이 공정한 채용을 위한 절차를 867차례 위반한 것으로 나타났다..?.미국 프로축구 메이저리그사커(mls) 인터 마이애미에서 활약 중인 아르헨티나 남자 축구 대표팀 공격수 리오넬 메시가 6일(한국시간) 미국 타임지가 선정한 ‘올해의 선수’로 뽑혔다. 메시는 세계 최고의 선수에게 주어지는 발롱도르를 올해 수상까지 총 8번 받은 '축구계 전설'이다. 지난해 겨울 카타르 월드컵에서 염원하던 월드컵 트로피를 조국 아르헨티나에 선사하기도 했다. 타임지는 \"메시가 인터 마이애미와 계약하면서 불가능해 보였던 일을 해냈다. 미국을 축구의 나라로 만들었다\"며 선정 배경을 알렸다..?.상대방을 ‘쿠바 총첩보국 후배’로 완전히 믿은 로차는 “몇 년이나 (쿠바 스파이로) 일했나”라고 묻자 “약 40년”이라고 답했다. fbi가 로차가 과거 비밀리에 칠레를 방문해 쿠바 총첩보국과 관계를 형성했다는 정보를 알고 수사를 시작한 것으로 보인다. 공소장에 따르면 연방수사국(fbi)은 지난해 로차가 쿠바 측의 스파이였다는 정보를 입수하고, 스페인어를 사용하는 수사관을 쿠바 총첩보국 요원인 것처럼 위장시켜 은퇴 후 플로리다주 마이애미에서 살고 있던 로차에게 접근시켰다. 로차는 “칠레에서부터 우리(쿠바)를 많이 도와주신 것으로 안다”는 fbi 수사관의 말에 경계심을 풀고 만남에 응했다고 한다. 미국 국무부, 백악관, 미군과 중남미 주재 미 대사관 등에서 27년간 중남미 담당 업무를 전담했던 베테랑 전직 외교관 빅터 마누엘 로차(73) 전 주볼리비아 미국대사가 쿠바를 위해 스파이 활동을 해온 혐의로 체포·기소됐다. 로차는 “칠레를 얘기하는 것을 보면 당신은 무슨 말을 들은 것이 틀림없다. 그 말에 신뢰를 갖게 됐다”고 말하며 fbi 위장 수사관에게 친밀감을 표시했다. 로차는 국무부 재직 당시 도미니카공화국·온두라스·멕시코 등 여러 중남미 공관에서 일했지만, 칠레에서 근무한 적은 없었다. fbi 위장 수사관이 ‘아바나’를 언급하자, 그는 “우리는 절대 ‘아바나’라고 말하지 않고 ‘그 섬’이라고 부른다”며 “만약 누군가 우리를 배신해서 적(미국)의 방첩기관에 말한다면…”이라고 상대를 조심시키기까지 했다. 미국 법무부는 로차가 약 40년간 쿠바의 정보기관인 총첩보국 비밀요원으로 활동해 왔다며 4일(현지 시각) 이같이 밝혔다. ‘칠레’는 로차를 체포하기 위해 fbi가 내건 미끼였다..?.tvn ‘유 퀴즈 온 더 블럭’에서 ‘뚝심’ 특집이 펼쳐진다..?.최근 달러 대비 원화 가치가 높은 상승세를 보이면서 앞으로 원·달러 환율이 어떻게 움직일지에 대한 투자자들의 관심이 커지고 있다. 그러나 전문가 4인은 모두 “원·달러 환율 하락세가 곧 멈출 것”으로 전망했다. 미국 기준금리 예측 모델인 시카고상품거래소(cme) 페드워치툴에 따르면 시장은 미국 연방준비제도(fed)가 내년에 0.25%포인트씩 4~5차례 금리를 낮출 것으로 기대하고 있는데 이는 연준이 제시한 점도표(금리 인상 예정표)보다 두 배 넘게 빠른 속도다..?.[osen=오세진 기자] 배우 차인표가 대학교 학생증 등 오래된 물건을 공개했다. 네티즌들은 \"진짜 멋지다\", \"내가 아내라면 매일 반할 듯\" 등 다양한 반응을 보였다.";
        System.out.println("dummy = " + dummy);
        String[] splits = dummy.split("\\.\\?\\.");

        List<String> convertSummary = new ArrayList<>();

        for (String split : splits) {
            convertSummary.add(split);
        }

        System.out.println("convertSummary = " + convertSummary.toString());
    }
}