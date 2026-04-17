export default function HomePage({ onStartGame }) {
  return (
    <div className="home-page">
      <div className="hero-section">
        <h1>Chess Game</h1>
        <p>Play chess against AI or challenge players online!</p>
      </div>

      <div className="game-modes">
        <div className="game-mode-card" onClick={() => onStartGame("vs_ai", "medium")}>
          <h2>Play vs Computer</h2>
          <p>Challenge the AI with adjustable difficulty</p>
          <button>Start Game</button>
        </div>

        <div className="game-mode-card" onClick={() => onStartGame("vs_human")}>
          <h2>Play Online</h2>
          <p>Challenge other players in real-time</p>
          <button>Find Match</button>
        </div>
      </div>

      <div className="features">
        <div className="feature">
          <h3>♟</h3>
          <h4>Smart AI</h4>
          <p>Multiple difficulty levels</p>
        </div>
        <div className="feature">
          <h3>♞</h3>
          <h4>Real-time</h4>
          <p>Play with opponents worldwide</p>
        </div>
        <div className="feature">
          <h3>♜</h3>
          <h4>Analysis</h4>
          <p>Review your games</p>
        </div>
      </div>
    </div>
  );
}