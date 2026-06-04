import { useState } from 'react'
import Start from "./components/Start"
import Game from "./components/Game"

function App() {
  const [screen, setScreen] = useState('START') // 'START' or 'PLAYING'
  const [level, setLevel] = useState('easy')

  const handleStartGame = (selectedLevel) => {
    setLevel(selectedLevel)
    setScreen('PLAYING')
  }

  const handleBackToTitle = () => {
    setScreen('START')
  }

  return (
    <div>
      {screen === 'START' ? (
        <Start onStartGame={handleStartGame} />
      ) : (
        <Game level={level} onBackToTitle={handleBackToTitle} />
      )}
    </div>
  )
}

export default App