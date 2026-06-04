import { useState, useEffect, useRef, useCallback } from 'react'
import styles from './Game.module.css'
import mockStages from '../mock/stages.json'

function Game({ level, onBackToTitle }) {
  // Game state: 'PLAYING', 'GAMEOVER', 'CLEAR'
  const [gameState, setGameState] = useState('PLAYING')
  const [stageData, setStageData] = useState(null)
  const [stagesCleared, setStagesCleared] = useState(0)
  const [timeLeft, setTimeLeft] = useState(60) // 60 seconds starting time
  const [regexInput, setRegexInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [totalAttempts, setTotalAttempts] = useState(0)
  const [correctAttempts, setCorrectAttempts] = useState(0)

  const timerRef = useRef(null)
  const usedStageIdsRef = useRef(new Set())

  const STAGES_TO_CLEAR = 5

  // Load a new stage
  const loadNewStage = useCallback(async () => {
    setLoading(true)
    setRegexInput('')

    try {
      // Try to fetch from backend
      const response = await fetch(`http://localhost:8090/api/v1/stages/generate?level=${level}`)
      if (!response.ok) {
        throw new Error(`HTTP status ${response.status}`)
      }
      const data = await response.json()
      setStageData(data)
      usedStageIdsRef.current.add(data.stage_id)
    } catch (err) {
      console.warn("Backend API failed, using mock stages:", err.message)
      // Fallback to mock data
      const candidates = mockStages[level] || mockStages['easy']
      // Try to pick one that hasn't been used yet in this run
      let selected = candidates.find(c => !usedStageIdsRef.current.has(c.stage_id))
      if (!selected) {
        // If all used, reset seen
        usedStageIdsRef.current.clear()
        selected = candidates[Math.floor(Math.random() * candidates.length)]
      }
      
      const uniqueId = `${selected.stage_id}-${Date.now()}`
      setStageData({
        ...selected,
        stage_id: uniqueId
      })
      usedStageIdsRef.current.add(uniqueId)
    } finally {
      setLoading(false)
    }
  }, [level])

  // Initial stage load
  useEffect(() => {
    const timerId = setTimeout(() => {
      loadNewStage()
    }, 0)

    // Start countdown timer
    timerRef.current = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          clearInterval(timerRef.current)
          setGameState('GAMEOVER')
          return 0
        }
        return prev - 1
      })
    }, 1000)

    return () => {
      clearTimeout(timerId)
      if (timerRef.current) clearInterval(timerRef.current)
    }
  }, [loadNewStage])

  // Derive simulator values during render
  let derivedSimStatus = 'WAITING'
  let derivedSimMatches = '-'
  let derivedErrorMessage = ''
  let derivedIsCorrect = false

  if (stageData && regexInput.trim()) {
    try {
      const patternText = regexInput.trim()
      // Evaluate matching behavior against noise_text
      const regex = new RegExp(patternText, 'gm')
      const noiseText = stageData.noise_text
      const correctString = stageData.correct_string

      // 1. Get all matches in noise text
      const matches = [...noiseText.matchAll(regex)].map(m => m[0])
      if (matches.length > 0) {
        derivedSimMatches = matches.join(', ')
      } else {
        derivedSimMatches = '(マッチなし)'
      }

      // 2. Evaluate correct/incorrect lines matching
      const lines = noiseText.split('\n')
      let matchedCorrectLine = false
      let matchedIncorrectLine = false

      lines.forEach(line => {
        const tempRegex = new RegExp(patternText, 'm')
        const hasMatch = tempRegex.test(line)
        const isCorrectLine = line.includes(correctString)

        if (isCorrectLine) {
          if (hasMatch) matchedCorrectLine = true
        } else {
          if (hasMatch) matchedIncorrectLine = true
        }
      })

      // 3. Pattern check (must match one of correct_patterns exactly or close enough)
      const isPatternCorrect = stageData.correct_patterns.some(p => p.trim() === patternText)
      const isMatchCorrect = matchedCorrectLine && !matchedIncorrectLine

      if (isPatternCorrect && isMatchCorrect) {
        derivedSimStatus = 'SUCCESS'
        derivedErrorMessage = ''
        derivedIsCorrect = true
      } else if (isMatchCorrect && !isPatternCorrect) {
        derivedSimStatus = 'CHEAT_PREVENTED'
        derivedErrorMessage = 'マッチ結果は正しいですが、問題の意図する正規表現パターンではありません。'
        derivedIsCorrect = false
      } else {
        derivedSimStatus = 'FAILED'
        derivedErrorMessage = matchedIncorrectLine ? 'ノイズ行に誤マッチしています。' : 'ターゲット行にマッチしていません。'
        derivedIsCorrect = false
      }

    } catch (err) {
      derivedSimStatus = 'SYNTAX ERROR'
      derivedSimMatches = '-'
      derivedErrorMessage = err.message
      derivedIsCorrect = false
    }
  }

  // Handle Submission
  const handleSubmit = () => {
    if (loading || !stageData) return

    setTotalAttempts(prev => prev + 1)
    
    if (derivedIsCorrect) {
      // Clear current stage
      setCorrectAttempts(prev => prev + 1)
      const newClearedCount = stagesCleared + 1
      setStagesCleared(newClearedCount)

      // Time bonus
      setTimeLeft(prev => prev + 15)

      if (newClearedCount >= STAGES_TO_CLEAR) {
        if (timerRef.current) clearInterval(timerRef.current)
        setGameState('CLEAR')
      } else {
        // Load next stage
        loadNewStage()
      }
    } else {
      // Penalty for wrong submit
      setTimeLeft(prev => Math.max(0, prev - 10))
      // Alert flash error visual
      const consoleBox = document.getElementById('consoleBox')
      if (consoleBox) {
        consoleBox.classList.add(styles.flashRed)
        setTimeout(() => consoleBox.classList.remove(styles.flashRed), 400)
      }
    }
  }

  // Handle Choice Select
  const handleChoiceClick = (choice) => {
    setRegexInput(choice)
  }

  // Restart Game
  const handleRestart = () => {
    setGameState('PLAYING')
    setStagesCleared(0)
    setTimeLeft(60)
    usedStageIdsRef.current.clear()
    setTotalAttempts(0)
    setCorrectAttempts(0)
    loadNewStage()
    // Restart timer
    if (timerRef.current) clearInterval(timerRef.current)
    timerRef.current = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          clearInterval(timerRef.current)
          setGameState('GAMEOVER')
          return 0
        }
        return prev - 1
      })
    }, 1000)
  }

  // Helper to highlight noise text in real time
  const renderHighlightedNoise = () => {
    if (!stageData) return ''

    const noiseText = stageData.noise_text
    const correctString = stageData.correct_string

    // Escape HTML to prevent XSS/rendering issues
    const escapeHtml = (text) => {
      return text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
    }

    if (!regexInput.trim()) {
      // No input: draw target string with a dashed border
      const escapedCorrect = escapeHtml(correctString)
      const lines = noiseText.split('\n')
      return lines.map((line, idx) => {
        const isCorrectLine = line.includes(correctString)
        const escapedLine = escapeHtml(line)
        if (isCorrectLine) {
          const parts = escapedLine.split(escapedCorrect)
          return (
            <div key={idx} className={styles.logLine}>
              {parts[0]}
              <span className={styles.targetDashed}>{escapedCorrect}</span>
              {parts[1]}
            </div>
          )
        }
        return <div key={idx} className={styles.logLine}>{escapedLine}</div>
      })
    }

    try {
      const lines = noiseText.split('\n')
      return lines.map((line, idx) => {
        const isCorrectLine = line.includes(correctString)

        // Split line by matches to highlight them
        const parts = line.split(new RegExp(`(${regexInput.trim()})`, 'g'))
        
        return (
          <div key={idx} className={styles.logLine}>
            {parts.map((part, pIdx) => {
              const matchesRegex = new RegExp(`^${regexInput.trim()}$`).test(part)
              if (matchesRegex) {
                return (
                  <span 
                    key={pIdx} 
                    className={isCorrectLine ? styles.matchCorrect : styles.matchIncorrect}
                  >
                    {escapeHtml(part)}
                  </span>
                )
              }
              return escapeHtml(part)
            })}
          </div>
        )
      })

    } catch {
      // Fallback on regex compile errors
      return noiseText.split('\n').map((line, idx) => (
        <div key={idx} className={styles.logLine}>{escapeHtml(line)}</div>
      ))
    }
  }

  // Render Game Over Screen
  if (gameState === 'GAMEOVER') {
    return (
      <div className={styles.overlayWrapper}>
        <div className={styles.overlayBox}>
          <div className={styles.glitchTitle} data-text="SYSTEM COMPROMISED">SYSTEM COMPROMISED</div>
          <h2 className={styles.gameOverHeading}>爆破阻止失敗...</h2>
          <p className={styles.overlayText}>
            制限時間内に正規表現解読コアをインストールできませんでした。<br />
            爆弾が爆発しました。
          </p>
          <div className={styles.statsContainer}>
            <div className={styles.statItem}>
              <span className={styles.statLabel}>クリアモジュール:</span>
              <span className={styles.statValue}>{stagesCleared} / {STAGES_TO_CLEAR}</span>
            </div>
            <div className={styles.statItem}>
              <span className={styles.statLabel}>正解率:</span>
              <span className={styles.statValue}>
                {totalAttempts > 0 ? Math.round((correctAttempts / totalAttempts) * 100) : 0}%
              </span>
            </div>
          </div>
          <div className={styles.overlayButtons}>
            <button type="button" className={styles.retryBtn} onClick={handleRestart}>
              RE-ATTEMPT / 再挑戦
            </button>
            <button type="button" className={styles.backBtn} onClick={onBackToTitle}>
              ABANDON / タイトルへ
            </button>
          </div>
        </div>
      </div>
    )
  }

  // Render Victory Screen
  if (gameState === 'CLEAR') {
    return (
      <div className={`${styles.overlayWrapper} ${styles.victoryBg}`}>
        <div className={`${styles.overlayBox} ${styles.victoryBox}`}>
          <div className={styles.victoryTitle}>BOMB DEFUSED</div>
          <h2 className={styles.victoryHeading}>爆破阻止完了！</h2>
          <p className={styles.overlayText}>
            すべての正規表現解読コアが正常に展開され、爆弾の信管が無効化されました。<br />
            ミッション成功です。
          </p>
          <div className={styles.statsContainer}>
            <div className={styles.statItem}>
              <span className={styles.statLabel}>残り時間:</span>
              <span className={styles.statValue}>{timeLeft} 秒</span>
            </div>
            <div className={styles.statItem}>
              <span className={styles.statLabel}>回答数 / ミス:</span>
              <span className={styles.statValue}>{totalAttempts}回 / {totalAttempts - correctAttempts}回</span>
            </div>
            <div className={styles.statItem}>
              <span className={styles.statLabel}>正解率:</span>
              <span className={styles.statValue}>
                {totalAttempts > 0 ? Math.round((correctAttempts / totalAttempts) * 100) : 0}%
              </span>
            </div>
          </div>
          <div className={styles.overlayButtons}>
            <button type="button" className={styles.victoryRetryBtn} onClick={handleRestart}>
              PLAY AGAIN / もう一度遊ぶ
            </button>
            <button type="button" className={styles.backBtn} onClick={onBackToTitle}>
              TITLE / タイトルへ
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className={styles.gameContainer}>
      {/* Top Banner Warning Status */}
      <div className={styles.statusBar}>
        <div className={styles.warningIndicator}>
          <span className={styles.warningDot}></span>
          <span className={styles.statusText}>
            {timeLeft < 15 ? 'ALERT: CRITICAL THREAT DETECTED' : 'SYSTEM STATUS: DEFUSAL PROTOCOL ACTIVE'}
          </span>
        </div>
        <div className={styles.difficultyIndicator}>
          LEVEL: {level.toUpperCase()}
        </div>
      </div>

      <div className={styles.mainLayout}>
        {/* Left Column: Work space */}
        <div className={styles.workspaceColumn}>
          {/* Progress & Timer */}
          <div className={styles.metaRow}>
            <div className={styles.progressBlock}>
              <span className={styles.metaLabel}>DECRYPTION PROGRESS:</span>
              <div className={styles.progressNodes}>
                {Array.from({ length: STAGES_TO_CLEAR }).map((_, idx) => (
                  <span 
                    key={idx} 
                    className={`${styles.progressNode} ${idx < stagesCleared ? styles.nodeCleared : ''} ${idx === stagesCleared ? styles.nodeActive : ''}`}
                  >
                    {idx < stagesCleared ? '✔' : idx + 1}
                  </span>
                ))}
              </div>
            </div>

            <div className={`${styles.timerBlock} ${timeLeft < 15 ? styles.timerAlert : ''}`}>
              <span className={styles.metaLabel}>TIME REMAINING:</span>
              <span className={styles.timerVal}>
                {String(Math.floor(timeLeft / 60)).padStart(2, '0')}:
                {String(timeLeft % 60).padStart(2, '0')}
              </span>
            </div>
          </div>

          {/* Prompt card */}
          <div className={styles.promptCard}>
            <div className={styles.cardHeader}>
              <span className={styles.cardTitle}>DECRYPTION OBJECTIVE (問題)</span>
              {stageData && <span className={styles.stageId}>ID: {stageData.stage_id.substring(0, 8)}</span>}
            </div>
            {loading ? (
              <div className={styles.loadingSpinnerContainer}>
                <span className={styles.spinner}></span>
                <span>Generating Signature...</span>
              </div>
            ) : (
              stageData && (
                <div className={styles.cardBody}>
                  <p className={styles.hintText}>{stageData.hint}</p>
                  <div className={styles.targetBlock}>
                    <span className={styles.targetLabel}>TARGET STRING:</span>
                    <span className={styles.targetValue}>{stageData.correct_string}</span>
                  </div>
                </div>
              )
            )}
          </div>

          {/* Choices Grid */}
          <div className={styles.choicesCard}>
            <div className={styles.cardHeader}>
              <span className={styles.cardTitle}>RECOMMENDED PATTERNS (選択肢 - クリックで代入)</span>
            </div>
            <div className={styles.choicesGrid}>
              {stageData?.choices.map((choice, index) => (
                <button 
                  key={index} 
                  type="button" 
                  className={`${styles.choiceBtn} ${regexInput === choice ? styles.choiceBtnActive : ''}`}
                  onClick={() => handleChoiceClick(choice)}
                >
                  <span className={styles.choiceCode}>{choice}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Regex Input & Simulation Console */}
          <div id="consoleBox" className={styles.consoleCard}>
            <div className={styles.cardHeader}>
              <span className={styles.cardTitle}>REGEX INJECTOR CONSOLE</span>
              <span className={`${styles.simBadge} ${styles['status_' + derivedSimStatus]}`}>
                {derivedSimStatus.replace('_', ' ')}
              </span>
            </div>
            <div className={styles.consoleBody}>
              <div className={styles.inputWrapper}>
                <span className={styles.regexPrefix}>/</span>
                <input 
                  type="text" 
                  className={styles.regexInputField}
                  value={regexInput}
                  onChange={(e) => setRegexInput(e.target.value)}
                  placeholder="正規表現を入力してください (例: ^\d{3}-\d{4}$)"
                />
                <span className={styles.regexSuffix}>/gm</span>
              </div>

              {/* Status details */}
              <div className={styles.statusDetails}>
                <div className={styles.matchesLine}>
                  <span className={styles.consoleLabel}>MATCHED:</span>
                  <span className={styles.consoleValue}>{derivedSimMatches}</span>
                </div>
                {derivedErrorMessage && (
                  <div className={styles.errorLine}>
                    <span className={styles.errorLabel}>DIAGNOSTICS:</span>
                    <span className={styles.errorText}>{derivedErrorMessage}</span>
                  </div>
                )}
              </div>

              {/* Action row */}
              <div className={styles.consoleActionRow}>
                <button 
                  type="button" 
                  className={styles.skipBtn}
                  onClick={loadNewStage}
                  disabled={loading}
                >
                  SKIP MODULE (-10s)
                </button>
                <button 
                  type="button" 
                  className={`${styles.submitBtn} ${derivedIsCorrect ? styles.submitBtnReady : ''}`}
                  onClick={handleSubmit}
                  disabled={loading || !regexInput}
                >
                  INJECT DECRYPTION KEY / 送信
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Log Monitor */}
        <div className={styles.logColumn}>
          <div className={styles.logMonitor}>
            <div className={styles.monitorHeader}>
              <span className={styles.monitorTitle}>SIGNAL LOG TERMINAL</span>
              <div className={styles.monitorStatus}>
                <span className={styles.blinkingDot}></span>
                <span>MONITORING STREAM</span>
              </div>
            </div>
            <div className={styles.monitorTerminal}>
              <div className={styles.scanline}></div>
              <div className={styles.terminalContent}>
                {loading ? (
                  <div className={styles.terminalLoading}>
                    <span>SCANNING CHANNELS...</span>
                  </div>
                ) : (
                  renderHighlightedNoise()
                )}
              </div>
            </div>
            <div className={styles.monitorFooter}>
              <span>GREEN: Target Match</span>
              <span>RED: Noise Match (Misfire)</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Game
