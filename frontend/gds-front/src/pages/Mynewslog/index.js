import Header from "../../components/Header/Header";
import LogMainview from "../../components/LogMainview/LogMainview";
import { useNavigate } from 'react-router-dom';
import { useEffect } from "react";

function Mynewslog() {

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
            <LogMainview />
        </>
    );
}

export default Mynewslog;