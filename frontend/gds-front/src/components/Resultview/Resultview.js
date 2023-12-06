import styles from './Resultview.module.css';
import SummaryText from '../../data/SummaryText';
import EachNews from '../../data/EachNews';
import React, { useEffect, useState } from 'react';

function Resultview({title, Data, Index}) {

    const [data, setData] = useState(EachNews);
    const [index, setIndex] = useState(0);

    const getSpeech = (text) => {
        let voices = [];

        //디바이스에 내장된 voice를 가져온다.
        const setVoiceList = () => {
          voices = window.speechSynthesis.getVoices();
        };
      
        setVoiceList();
      
        if (window.speechSynthesis.onvoiceschanged !== undefined) {
          //voice list에 변경됐을때, voice를 다시 가져온다.
          window.speechSynthesis.onvoiceschanged = setVoiceList;
        }
      
        const speech = (txt) => {
          const lang = "ko-KR";
          const utterThis = new SpeechSynthesisUtterance(txt);
      
          utterThis.lang = lang;
      
          /* 한국어 vocie 찾기
             디바이스 별로 한국어는 ko-KR 또는 ko_KR로 voice가 정의되어 있다.
          */
          const kor_voice = voices.find(
            (elem) => elem.lang === lang || elem.lang === lang.replace("-", "_")
          );
      
          //힌국어 voice가 있다면 ? utterance에 목소리를 설정한다 : 리턴하여 목소리가 나오지 않도록 한다.
          if (kor_voice) {
            utterThis.voice = kor_voice;
          } else {
            return;
          }
      
          //utterance를 재생(speak)한다.
          window.speechSynthesis.speak(utterThis);
        };
      
        speech(text);
    }

    useEffect(() => {
        window.speechSynthesis.getVoices();

        if (typeof Data !== 'undefined') {
            setData(Data);
            console.log("Data: ", Data);
        }

        if (typeof Index !== 'undefined') {
            setIndex(Index);
        }

    }, [Data, Index]);

    const listenNews = () => {
        console.log("## 뉴스 듣기 버튼 누름 ##")
        var tmp = ""

        data[index].summary.map((text) => (
            tmp = tmp + '\n' + text
        ))
        getSpeech(tmp)
    }

    const stopListen = () => {
        console.log("## 듣기 멈춤 버튼 누름 ##")
        window.speechSynthesis.cancel();
    }

    const handleEachNews = (idx) => {
        const link = data[index].news[idx].link;
        if (link) {
            window.open(link, '_blank');
        }
    }

    return (
        <div className={styles.resultViewDiv}>
            <h2 className={styles.title}>{localStorage.getItem('UserName')+title}</h2>
            <div className={styles.mainView}>
                <div className={styles.outerView}>
                    <div className={styles.innerView}>
                        {data[index].summary?.map((text) => (
                            <p className={styles.summaryText}>
                                &nbsp;{text}
                            </p>
                        ))}
                    </div>
                </div>
                <div className={styles.eachNewsDiv}>
                    <ul>
                        {data[index].news?.map((item, index) => (
                            <li className={styles.eachNews} onClick={() => handleEachNews(index)}>
                                <p>
                                    <p><h4>{item.title}</h4></p>
                                    <p>
                                        &nbsp;{item.context.length > 30 ? item.context.substring(0, 100).replace(/\.?\./g, "") + "..." : item.context}
                                    </p>
                                    <p className={styles.mediaP}>
                                        {item.companyName}
                                    </p>
                                </p>
                            </li>
                        ))}
                    </ul>
                </div>
                <div className={styles.btnDiv}>
                    <button className={styles.listenBtn} onClick={listenNews}>
                        뉴스<br />듣기
                    </button>
                    <br/>
                    <button className={styles.listenBtn} onClick={stopListen}>
                        듣기<br />멈춤
                    </button>
                </div>
            </div>
        </div>
       
    );
}

export default Resultview;