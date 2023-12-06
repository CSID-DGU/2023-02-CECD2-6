import React, { useState } from 'react';
import DatePicker from 'react-datepicker'; // 캘린더 기능을 제공하는 패키지
import 'react-datepicker/dist/react-datepicker.css'; // 스타일 시트
import styles from './CalendarComponents.module.css';

function CalendarComponent({ handleDateSelect }) {
  const [selectedDate, setSelectedDate] = useState(null);

  const handleDateChange = (date) => {
    setSelectedDate(date);
    handleDateSelect(date); // 선택한 날짜를 부모 컴포넌트로 전달
  };

  return (
    <DatePicker
      selected={selectedDate}
      onChange={handleDateChange}
      dateFormat="yyyy.MM.dd" // 날짜 형식 지정 (원하는 형태로 변경 가능)
      shouldCloseOnSelect
      className={styles.DatePicker}
    />
  );
}

export default CalendarComponent;