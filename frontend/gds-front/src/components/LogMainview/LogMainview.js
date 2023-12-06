import Resultview from "../../components/Resultview/Resultview";
import NewsLogTable from "../NewsLogTable/NewsLogTable";
import styles from './LogMainview.module.css';
import React, { useState, useEffect } from 'react';
import { instance } from "../../apis";

function LogMainview() {

    const [log, setLog] = useState();
    const [index, setIndex] = useState();

    const handleIndexChange = (index) => {
        setIndex(index);
        console.log("NewsLogTable이 준 index: ", index);
    }

    useEffect(() => {
        const fetchUserData = async() => {
            try {
                const response = await instance.get(
                    `/summary/getusersummary?id=${localStorage.getItem('UserID')}`,
                    {
                        withCredentials: true,
                        headers: {
                          "Content-Type": "application/json",
                        },
                    }
                );
                console.log("유저 이전 뉴스듣기 로그 정보 GET 성공!", response.data);
                setLog(response.data);
        
            } catch(error) {
                console.error("유저 이전 뉴스듣기 로그 정보 GET 실패!", error);
                alert("유저 이전 뉴스듣기 로그 정보 GET 실패!\n");
            }
          }
          fetchUserData();
        
    }, []);

    return (
        <div className={styles.logMainView}>
            <h2>이전 뉴스듣기 기록</h2>
            <NewsLogTable onIndexChange={handleIndexChange} logData={log} />
            <Resultview title="님이 선택한 관심분야, 키워드에 따른 뉴스 요약 내용" Data={log} Index={index} />
            <br/><br/>
        </div>
    );
}

export default LogMainview;