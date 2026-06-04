import styles from './Start.module.css'
import kigouImage from '../assets/kigou.png'

const warningText = Array(20).fill('WARNING').join('')

function Start() {
  return (
    <div className={styles.wrapper}>
      <div className={styles.topArea}>
        <div className={styles.top}>
          <span className={styles.warningText}>{warningText}</span>
        </div>
        <div className={styles.logoArea}>
          <div className={styles.logoWrapper}>
            <img className={styles.kigouImage} src={kigouImage} alt="kigou" />
            <div className={styles.titleBlock}>
              <h2 className={styles.title}>Regex</h2>
              <p className={styles.subtitle}>- レジェックス -</p>
              <p className={styles.description}>記憶の力で、爆破を阻止しよう</p>
            </div>
          </div>
        </div>
      </div>
      <div className={styles.bottom}>
        <span className={styles.warningText}>{warningText}</span>
      </div>
    </div>
  )
}

export default Start