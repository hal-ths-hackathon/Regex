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
            <h2 className={styles.title}>Regex</h2>
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