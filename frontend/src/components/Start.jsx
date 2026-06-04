import styles from './Start.module.css'
import warningImage from '../assets/warning.png'
import kigouImage from '../assets/kigou.png'

function Start() {
  return (
    <div className={styles.wrapper}>
      <div className={styles.topArea}>
        <div className={styles.top}>
          <img className={styles.warningImage} src={warningImage} alt="warning" />
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
        <img className={styles.warningImage} src={warningImage} alt="warning" />
      </div>
    </div>
  )
}

export default Start