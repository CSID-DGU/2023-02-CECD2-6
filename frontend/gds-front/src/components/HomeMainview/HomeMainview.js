import Resultview from "../../components/Resultview/Resultview";
import Categorybar from "../../components/Categorybar/Categorybar";
import Keywordbar from "../../components/Keywordbar/Keywordbar";
import styles from './HomeMainview.module.css';
import { useState, useEffect } from "react";
import { instance } from "../../apis";
import Loading from "../Loading/Loading";

function HomeMainview() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);
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

    const handleanotherNewsBtn = async() => {
        //API
        if (selectedCategoriesList.length === 0 && registeredKeywordsList.length === 0) {
            alert('분야/키워드 중 한 항목은 비어있지 않아야합니다!');
            return; // 필드가 비어있으면 요청을 하지 않습니다.
        }

        try {

            setLoading(true);

            const topics = [];
            selectedCategoriesList.map((item) => {
                topics.push(Categories[item])
            })

            console.log("다른 뉴스 듣기 요청!!");
            console.log("topic: ", topics)

            const response = await instance.post(
                `/summary/instant`,
                {
                    userId: localStorage.getItem('UserID'),
                    categories: topics,
                    keywords: registeredKeywordsList,
                },
                {
                    withCredentials: true,
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            );
            console.log("다른 뉴스 듣기 요청 성공!", response.data);
            setData(response.data);
            setLoading(false);

        } catch(error) {
            console.error("다른 뉴스 듣기 요청 실패!", error);
            alert("다른 뉴스 듣기 요청 실패!\n");
        }
    }

    useEffect(() => {
        const fetchUserData = async() => {
            try {
                const response = await instance.get(
                    `/summary/getlastbatchsummary?id=${localStorage.getItem('UserID')}`,
                    {
                        withCredentials: true,
                        headers: {
                          "Content-Type": "application/json",
                        },
                    }
                );
                console.log("최신 뉴스듣기 정보 GET 성공!", response.data);
                setData(response.data);
        
            } catch(error) {
                console.error("최신 뉴스듣기 정보 GET 실패!", error);
                alert("유저 이전 뉴스듣기 로그 정보 GET 실패!\n");
            }
          }
          fetchUserData();
        
    }, []);

    return (
        <div className={styles.homeMainView}>
            {loading ? (
                <Loading />
            ) : (
                <div>
                    <Resultview title="님이 선택한 관심분야, 키워드에 따른 뉴스 요약 내용" Data={[data]} />
                    <br/><h2>다른 뉴스 요약 듣기</h2>
                    <Categorybar onSelectCategories={handleSelectedCategories} />
                    <br/>
                    <div className={styles.anotherNewsDiv}>
                        <Keywordbar onRegisterKeywords={handleRegisteredKeywords}/>
                        <button className={styles.anotherNewsBtn} onClick={handleanotherNewsBtn}>다른 뉴스 요약 듣기</button>
                    </div>
                    <br/><br/>
                </div>
            )}            
        </div>
    );
}

export default HomeMainview;