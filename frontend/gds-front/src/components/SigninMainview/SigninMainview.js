import React, { useState } from 'react';
import styles from './SigninMainview.module.css';
import CustomInput from "../CustomInput/CustomInput";
import logoImg from "../../assets/images/mixedLogo.png";
import { useNavigate } from 'react-router-dom';
import { instance } from "../../apis";

function SigninMainview() {

    const [userID, setUserID] = useState();
    const [userPWD, setUserPWD] = useState();
    const navigate = useNavigate();

    const handleUserIDChange = (value) => {
        setUserID(value);
    };

    const handleUserPWDChange = (value) => {
        setUserPWD(value);
    };

    const handleSignInBtn = async () => {
        console.log('UserID: ', userID);
        console.log('UserPWD: ', userPWD);

        if (!userID || !userPWD) {
            console.error('UserID나 UserPWD가 비어 있습니다.');
            alert('UserID나 UserPWD가 비어 있습니다.');
            return; // 필드가 비어있으면 요청을 하지 않습니다.
        }

        try {
            const response = await instance.post(
                `/usersign/sign-in`,
                {
                    accountId: userID,
                    password: userPWD,
                },
                {
                    withCredentials: true,
                    headers: {
                      "Content-Type": "application/x-www-form-urlencoded",
                    },
                }
            );            
            alert("로그인 성공");
            localStorage.setItem("UserID", response.data.userId);
            localStorage.setItem("UserName", response.data.name);
            localStorage.setItem("isKeywordRegistered", response.data.keywords);
            localStorage.setItem("isCategoryRegistered", response.data.categories);

            if (localStorage.getItem("isKeywordRegistered") === 'true' || localStorage.getItem("isCategoryRegistered") === 'true') {
                navigate("/home");
            } else {
                alert("분야/키워드 설정을 진행해주세요!");
                navigate("/mypage");
            }

        } catch(error) {
            console.error("로그인 실패:", error);
        }
    }
    
    return (
        <div className={styles.mainView}>
            <h2 className={styles.title}>로그인</h2>
            <div className={styles.outerView}>
                <div className={styles.innerView}>
                    <div className={styles.logoImg}>
                        <img src={logoImg} alt='logoImg' id={styles.logoImg}/>
                    </div>
                    <div className={styles.signinInput}>
                        <CustomInput Text="id" onValueChange={handleUserIDChange}/>
                        <CustomInput Text="비밀번호" type="password" onValueChange={handleUserPWDChange}/>                        
                    </div>
                    <div className={styles.signinBtnView}>
                        <button className={styles.signInBtn} onClick={handleSignInBtn}>
                            로그인
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default SigninMainview;