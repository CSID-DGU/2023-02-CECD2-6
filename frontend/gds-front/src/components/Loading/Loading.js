import React from 'react';
import {TailSpin} from "react-loader-spinner";
import styles from './Loading.module.css';

function Loading() {
    return (
        <div className={styles.loadingDiv}>
            <TailSpin
                color='#FDD874'
                height={200}
                width={200}
                margin={50}
            />
            <div className={styles.loadingTextDiv}>잠시만 기다려주세요!</div>
        </div>
    );
};
    
export default Loading;