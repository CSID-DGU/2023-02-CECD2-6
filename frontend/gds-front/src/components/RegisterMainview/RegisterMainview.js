import React, { useState } from 'react';
import styles from './RegisterMainview.module.css';
import CustomInput from "../CustomInput/CustomInput";
import DatePicker from 'react-datepicker'; // 캘린더 기능을 제공하는 패키지
import 'react-datepicker/dist/react-datepicker.css';
import { ko } from "date-fns/esm/locale";
import { useNavigate } from 'react-router-dom';
import { instance } from "../../apis";

function RegisterMainview() {

    const navigate = useNavigate();
    const [userID, setUserID] = useState();
    const [userPWD, setUserPWD] = useState();
    const [userPWDCheck, setUserPWDCheck] = useState();
    const [userName, setUserName] = useState();
    const [userBirth, setUserBirth] = useState(new Date());

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

    const handleUserIDChange = (value) => {
        setUserID(value);
    };

    const handleUserPWDChange = (value) => {
        setUserPWD(value);
    };

    const handleUserPWDCheckChange = (value) => {
        setUserPWDCheck(value);
    };

    const handleUserNameChange = (value) => {
        setUserName(value);
    };

    const handleRegisterBtn = async() => {
        console.log('UserID: ', userID);
        console.log('UserPWD: ', userPWD);
        console.log('userPWDCheck: ', userPWDCheck);
        console.log('userName: ', userName);
        console.log('userBirth: ', formatDate(userBirth));

        if (!userID || !userPWD || !userPWDCheck || !userName || !userBirth) {
            alert('비어있는 항목이 있습니다!');
            return; // 필드가 비어있으면 요청을 하지 않습니다.
        }

        try {
            const response = await instance.post(
                `/usersign/sign-up`,
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
            alert("회원가입 성공!");
            console.log("회원가입 성공!", response);
            navigate("/");

        } catch(error) {
            console.error("회원가입 실패!", error.response.data);
            alert("회원가입 실패!\n" + error.response.data);
        }
    }

    return (
        <div className={styles.mainView}>
            <h2 className={styles.title}>회원가입</h2>
            <div className={styles.outerView}>
                <div className={styles.innerView}>
                    <CustomInput Text="id" onValueChange={handleUserIDChange}/>
                    <CustomInput Text="비밀번호" type="password" onValueChange={handleUserPWDChange}/>
                    <CustomInput Text="비밀번호 확인" type="password" onValueChange={handleUserPWDCheckChange}/>
                    <CustomInput Text="이름" onValueChange={handleUserNameChange}/>
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
                        <button className={styles.registerBtn} onClick={handleRegisterBtn}>
                            가입하기
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default RegisterMainview;