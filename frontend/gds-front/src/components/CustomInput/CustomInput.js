import styles from './CustomInput.module.css';

function CustomInput({Text, onValueChange, type, inputText}) {

    const handleChange = (event) => {
        onValueChange(event.target.value);
    }

    return (
        <p>
            <label className={styles.customLabel}>{Text}</label>
            <input 
                type={type === 'password' ? type : 'text'}
                className={styles.customInput}
                onChange={handleChange}
                value={inputText === null ? null : inputText}
            />
        </p>
    );
}

export default CustomInput;