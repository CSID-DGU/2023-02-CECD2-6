import React, { useState, useEffect } from 'react';
import styles from './Keywordbar.module.css';

function Keywordbar({ onRegisterKeywords }) {

    const [inputText, setInputText] = useState('');
    const [registeredKeywords, setRegisteredKeywords] = useState([]);

    const handleKeywordRegister = () => {
        if (inputText.trim() !== '') {
            setRegisteredKeywords(prevKeywords => [...prevKeywords, inputText]);
            setInputText('');
        }
    }

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            handleKeywordRegister();
        }
    }

    const handleSpanDoubleClick = (index) => {
        setRegisteredKeywords(prevKeywords => prevKeywords.filter((_, i) => i !== index));
    }

    useEffect(() => {
        onRegisterKeywords(registeredKeywords);
    }, [registeredKeywords, onRegisterKeywords])

    return (
        <div className={styles.mainDiv}>
            <div className={styles.keywordBar}>
                <div className={styles.titleDiv}>
                    <div className={styles.titleText}>
                        키워드<br />등록
                    </div>
                </div>
                <div className={styles.registeredDiv}>
                    {registeredKeywords.map((keyword, index) => (
                        <div
                        className={styles.keywordDiv}
                            key={index}
                            onDoubleClick={() => handleSpanDoubleClick(index)}
                        >
                            {keyword}
                        </div>
                    ))}
                </div>
            </div>
            <div className={styles.inputDiv}>                
                <input 
                    type='text'
                    className={styles.customInput}
                    placeholder="  키워드를 입력하세요!"
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    onKeyDown={handleKeyDown}
                />
                <button className={styles.registerBtn} onClick={handleKeywordRegister}>등록</button>
            </div>
        </div>
    );
}

export default Keywordbar;