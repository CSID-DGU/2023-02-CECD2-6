import React, { useState, useEffect } from 'react';
import styles from './NewsLogTable.module.css';
import NewsLogData from '../../data/NewsLogData';
import { instance } from "../../apis";

function NewsLogTable({logData, onIndexChange}) {
    
    const [log, setLog] = useState(NewsLogData);

    const handleEachLog = (index) => {
        onIndexChange(index);
        console.log("선택된 index: ", index);
    }

    useEffect(()=>{
        if (logData) {
            setLog(logData);
         }
    }, [logData]);

    return (
        <div className={styles.tableDiv}>
           <ul>
                <div className={styles.titleDiv}>
                    <div className={styles.dataDiv}>날짜</div>
                    <div className={styles.dataDiv}>시간</div>
                    <div className={styles.dataDiv}>분야</div>
                    <div className={styles.keywordDiv}>키워드</div>
                </div>
                <div className={styles.newsLogDiv}>
                    {log.map((item, index) => (
                        <li key={index} className={styles.eachNewsLog} onClick={() => handleEachLog(index)}>
                            <div className={styles.dataDiv}>{new Date(item.createdTime).toLocaleDateString()}</div>
                            <div className={styles.dataDiv}>{new Date(item.createdTime).toLocaleTimeString()}</div>
                            <div className={styles.dataDiv}>{item.categories === null ? '미선택' : item.categories}</div>
                            <div className={styles.keywordDiv}>{item.keywords === null ? '미선택' : item.keywords}</div>
                        </li>
                    ))}
                </div>
            </ul>
        </div>
    );
}

export default NewsLogTable;