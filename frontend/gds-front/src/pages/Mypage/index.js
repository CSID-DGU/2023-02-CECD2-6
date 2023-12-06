import Header from "../../components/Header/Header";
import TabComponent from "../../components/Tab/Tab";
import { useNavigate } from 'react-router-dom';
import { useEffect } from "react";

function Mypage() {
    
    const navigate = useNavigate();

    useEffect(() => {
        const isLoggedIn = localStorage.getItem('UserID');
        if (isLoggedIn === null) {
            console.log('비로그인 중', isLoggedIn);
            alert("로그인이 필요합니다!");
            navigate("/");
        } else {
            console.log('로그인 중', isLoggedIn);
        }
    }, [navigate]);

    return (
        <>  
            <Header />
            <TabComponent />
        </>
    );
}

export default Mypage;