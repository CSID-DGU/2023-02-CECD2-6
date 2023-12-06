import React, { useEffect, useState } from 'react';
import styles from './Tab.module.css';
import Keywordbar from '../Keywordbar/Keywordbar';
import Categorybar from '../Categorybar/Categorybar';
import CustomInput from '../CustomInput/CustomInput';
import { ko } from "date-fns/esm/locale";
import { instance } from "../../apis";
import DatePicker from 'react-datepicker';


const TabComponent = () => {

  const [userID, setUserID] = useState();
  const [userPWD, setUserPWD] = useState();
  const [userPWDCheck, setUserPWDCheck] = useState();
  const [userName, setUserName] = useState();
  const [userBirth, setUserBirth] = useState(new Date());

  useEffect(() => {
    const fetchUserData = async() => {
      try {
          const response = await instance.get(
              `/user/info?id=${localStorage.getItem('UserID')}`,
              {
                  withCredentials: true,
                  headers: {
                    "Content-Type": "application/json",
                  },
              }
          );
          console.log("유저 정보 GET 성공!", response);
          setUserID(response.data.userId);
          setUserName(response.data.name);

          const dateString = response.data.birth;
          const dateParts = dateString.split("-");
          setUserBirth(new Date(dateParts[0], dateParts[1] -1, dateParts[2]));

  
      } catch(error) {
          console.error("유저 정보 GET  실패!", error);
          alert("유저 정보 GET  실패!\n");
      }
    }
    fetchUserData();
  },[]);

  const handleUserPWDChange = (value) => {
    setUserPWD(value);
  };

  const handleUserPWDCheckChange = (value) => {
      setUserPWDCheck(value);
  };

  const handleUserNameChange = (value) => {
      setUserName(value);
  };

  function formatDate(date) {
    const year = date.getFullYear();
    let month = date.getMonth() + 1;
    let day = date.getDate();
  
    if (month < 10) {
      month = `0${month}`;
    }
    if (day < 10) {
      day = `0${day}`;
    }
  
    return `${year}-${month}-${day}`;
  }

  const [activeTab, setActiveTab] = useState(0); // 활성화된 탭의 인덱스를 관리하는 상태
  const [selectedCategoriesList, setSelectedCategoriesList] = useState([]);
  const [registeredKeywordsList, setRegisteredKeywordsList] = useState([]);
  const Categories = ['전체', '정치', '경제', '사회', '국제', '문화', '오피니언', '스포츠', '연예'];

  const handleSelectedCategories = (categories) => {
    setSelectedCategoriesList(categories);
    console.log("selectedCategoriesList in Tab.js", selectedCategoriesList)
  };

  const handleRegisteredKeywords = (keywords) => {
    setRegisteredKeywordsList(keywords);
    console.log("registeredKeywords in Tab.js", registeredKeywordsList)
  };

  const handleSaveBtn = async() => {
    //API
    if (selectedCategoriesList.length === 0 || registeredKeywordsList.length === 0) {
      alert('비어있는 항목이 있습니다!');
      return; // 필드가 비어있으면 요청을 하지 않습니다.
    }

    try {
        const topics = [];
        selectedCategoriesList.map((item) => {
          topics.push(Categories[item])
        })

        console.log("topic: ", topics)

        const response = await instance.post(
            `/user/register`,
            {
                userId: localStorage.getItem('UserID'),
                topics: topics,
                keywords: registeredKeywordsList,
            },
            {
                withCredentials: true,
                headers: {
                  "Content-Type": "application/json",
                },
            }
        );            
        alert("분야/키워드 저장 성공!");
        console.log("분야/키워드 저장 성공!", response);

    } catch(error) {
        console.error("분야/키워드 저장 실패!", error);
        alert("분야/키워드 저장 실패!\n");
    }
  }

  const handleEditBtn = async() => {
    //API
    if (!userID || !userPWD || !userPWDCheck || !userName || !userBirth) {
      alert('비어있는 항목이 있습니다!');
      return; // 필드가 비어있으면 요청을 하지 않습니다.
    }

    try {
        const response = await instance.post(
            `/usersign/modify`,
            {
              accountId: userID,
              name: userName,
              password: userPWD,
              checkedPassword: userPWDCheck,
              birth: formatDate(userBirth),
            },
            {
                withCredentials: true,
                headers: {
                  "Content-Type": "application/x-www-form-urlencoded",
                },
            }
        );            
        alert("유저 정보 수정 성공!");
        console.log("유저 정보 수정 성공!", response);

    } catch(error) {
        console.error("유저 정보 수정  실패!", error);
        alert("유저 정보 수정  실패!\n");
    }
  }

  // 클릭 이벤트 핸들러: 해당 탭의 인덱스를 받아 활성화된 탭을 변경
  const handleTabClick = (index) => {
    setActiveTab(index);
  };

  // 각 탭을 렌더링하는 함수
  const renderTabs = () => {
    const tabs = ['분야/키워드 설정', '회원정보수정']; // 탭의 제목 등 정보를 포함하는 배열

    return tabs.map((tab, index) => (
      <div
        key={index}
        onClick={() => handleTabClick(index)}
        style={activeTab === index ? { backgroundColor: '#FDD874'} : { backgroundColor: '#EDE8E8'}}
      >
        {tab}
      </div>
    ));
  };

  // 각 탭 내용을 렌더링하는 함수
  const renderTabContent = () => {
    return (
        activeTab === 0 ? (
          <>
              <div className={styles.innerView}>
                  <Categorybar onSelectCategories={handleSelectedCategories}/>
                  <br /><br />
                  <Keywordbar onRegisterKeywords={handleRegisteredKeywords} />
                  <button className={styles.saveBtn} onClick={handleSaveBtn}>
                              저장하기
                  </button>
              </div>
          </>
      ) : (
            <>
                <div className={styles.innerView}>
                    <p>
                        <label className={styles.customLabel}>id</label>
                        <input type='text' className={styles.idInput} readOnly value={localStorage.getItem('UserID') === null ? 'Error' : userID}/>
                    </p>
                    <CustomInput Text="비밀번호" onValueChange={handleUserPWDChange} type="password" />
                    <CustomInput Text="비밀번호 확인" onValueChange={handleUserPWDCheckChange} type="password"/>
                    <CustomInput Text="이름" onValueChange={handleUserNameChange} inputText={userName}/>
                    <p>
                        <label className={styles.customLabel}>생년월일</label>
                        <DatePicker
                            locale={ko}
                            selected={userBirth}
                            onChange={(date) => setUserBirth(date)}
                            dateFormat="yyyy-MM-dd"
                            wrapperClassName={styles.datePicker}
                    />
                    </p>
                    <div>
                        <button className={styles.editBtn} onClick={handleEditBtn}>
                            수정하기
                        </button>
                    </div>
                </div>
            </>
        )
    );
  };

  return (
    <div className={styles.mainDiv}>
      <h2>마이페이지</h2>
      <div className={styles.tabHeader}>{renderTabs()}</div>
      <div className={styles.tabContent}>{renderTabContent()}</div>
    </div>
  );
};

export default TabComponent;
