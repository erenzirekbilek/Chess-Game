export default function GameOverModal({ result, onPlayAgain, onGoHome }) {
  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>Game Over</h2>
        <div className="result-display">
          {result === "You Win!" && <span className="win">♔ You Win!</span>}
          {result === "You Lose!" && <span className="lose">♚ You Lose!</span>}
          {result === "Draw!" && <span className="draw">♛ Draw!</span>}
          {result === "You Resigned!" && <span className="resigned">You Resigned</span>}
        </div>
        <div className="modal-actions">
          <button onClick={onPlayAgain}>Play Again</button>
          <button onClick={onGoHome}>Main Menu</button>
        </div>
      </div>
    </div>
  );
}