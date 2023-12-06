import { Link, useNavigate } from 'react-router-dom';
import imageLogo from '../../assets/images/imageLogo.png';
import textLogo from '../../assets/images/textLogo.png';
import userImg from '../../assets/images/user.png';

import styles from './Header.module.css';

function Header() {

    const navigate = useNavigate();
    const isLoggedIn = localStorage.getItem('UserID');

    const handleSigninClick = () => {
        navigate('/')
    }

    const handleSignupClick = () => {
        navigate('/signup')
    }

    const handleLogoutClick = () => {
        //세션에서 로그인정보 지우기
         localStorage.removeItem('UserID');
        navigate('/')
    }

    const handleUserClick = () => {
        navigate('/mypage')
    }

    const hadleClickLogo = () => {

        if (localStorage.getItem('UserID') === null) {
            navigate('/')
        }
        else navigate('/home')
    }

    return (
        <header className={styles.header}>
            <div className={styles.topSection}>
                <div className={styles.logoSection} onClick={hadleClickLogo}>
                    <img src={imageLogo} alt='ImageLogo' id={styles.imageLogo}/>
                    <img src={textLogo} alt='TextLogo' id={styles.textLogo}/>
                </div>
                <div className={styles.btnSection}>
                    {isLoggedIn != null ? (
                        <>
                            <button className={styles.headerBtn} onClick={handleLogoutClick}>LOGOUT</button>
                            <img src={userImg} alt='userImg' id={styles.userImg} onClick={handleUserClick}/>
                        </>
                    ) : (
                        <>
                            <button className={styles.headerBtn} onClick={handleSigninClick}>SIGN IN</button>
                            <button className={styles.headerBtn} onClick={handleSignupClick}>SIGN UP</button>
                        </>
                    )}              
                </div>
            </div>
            <div className={styles.navContainer}>
                <nav className={styles.mainNav}>
                    <Link to='/home'className={styles.active}>Home</Link>
                    <Link to='/mynewslog' className={styles.active}>MyNewsLog</Link>
                    <Link to='/about' className={styles.active}>About</Link>
                </nav>
            </div>
        </header>
    );
}

export default Header;