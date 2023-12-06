import React, { useState, useEffect } from 'react';
import styles from './Categorybar.module.css'
import allImg from '../../assets/images/categoryItems/all.png'
import politicsImg from '../../assets/images/categoryItems/politics.png'
import economyImg from '../../assets/images/categoryItems/economy.png'
import societyImg from '../../assets/images/categoryItems/society.png'
import internationalImg from '../../assets/images/categoryItems/international.png'
import cultureImg from '../../assets/images/categoryItems/culture.png'
import opinionImg from '../../assets/images/categoryItems/opinion.png'
import sportsImg from '../../assets/images/categoryItems/sports.png'
import entertainmentImg from '../../assets/images/categoryItems/entertainment.png'

function Categorybar({ onSelectCategories }) {

    const [selectedCategories, setSelectedCategories] = useState([]);
    const imgList = [allImg, politicsImg, economyImg, societyImg, internationalImg, cultureImg, opinionImg, sportsImg, entertainmentImg]


    const handleCategoryClick = (index) => {
        const isSelected = selectedCategories.includes(index);
        setSelectedCategories(isSelected ? selectedCategories.filter(item => item !== index) : [...selectedCategories, index]);
    };

    const selectStyle = (index) => {
        return selectedCategories.includes(index) ? { borderBottom: '2px solid #ffb300' } : {};
    };

    useEffect(() => {
        onSelectCategories(selectedCategories);
    }, [selectedCategories, onSelectCategories])

    return (
        <div className={styles.mainDiv}>
            <div className={styles.categoryBar}>
                <div className={styles.titleDiv}>
                    <p>
                        분야<br />선택
                    </p>
                </div>
                <div className={styles.selectDiv}>
                    {['전체', '정치', '경제', '사회', '국제', '문화', '오피니언', '스포츠', '연예'].map((category, index) => (
                        <div key={index} className={styles.eachSelect} style={selectStyle(index)} onClick={() => handleCategoryClick(index)}>
                            {/* 각 카테고리 이미지 및 텍스트 */}
                            <img src={`${imgList[index]}`} alt={`${imgList[index]}.png`} />
                            <br />
                            <span>{category}</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default Categorybar;