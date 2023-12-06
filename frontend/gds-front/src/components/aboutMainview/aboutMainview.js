import imageLogo from '../../assets/images/imageLogo.png';
import textLogo from '../../assets/images/textLogo.png';
import styles from './aboutMainview.module.css';

function aboutMainview() {
    return(
        <div className={styles.aboutMainView}>
            <h2>서비스 소개</h2>
            <div className={styles.logoSection}>
                <img src={imageLogo} alt='ImageLogo' id={styles.imageLogo}/>
                <img src={textLogo} alt='TextLogo' id={styles.textLogo}/>
            </div>
            <br/><br/>
            <h2>서비스 개요</h2>
            <div className={styles.introSection}>
                <p>
                &nbsp;서비스 LET'S SUMMARY! 는 사용자의 관심사에 따른 뉴스를 제공합니다.
                사용자는 자신이 관심있는 분야와 키워드를 설정하고, 해당 정보를 바탕으로 최신 뉴스들에 대한 
                요약문과 이에 대한 TTS 서비스를 제공받을 수 있는 서비스입니다. 비슷한 주제의 다양한 뉴스들을 
                요약된 본문을 직접 읽어주는 서비스도 제공합니다.
                </p>
            </div>
            <br/><br/>
            <h2>서비스 주요 기능 소개</h2>
            <div className={styles.mainFuncSection}>
                <p>
                    1. 사용자가 선택한 분야와 키워드에 대한 요약문을 제공해드립니다.
                </p>
                <p>
                    2. 제공된 요약문을 사용자는 듣기버튼을 통해서 청취할 수 있습니다.
                </p>
            </div>
            <br/><br/>
        </div>
    );
}

export default aboutMainview;