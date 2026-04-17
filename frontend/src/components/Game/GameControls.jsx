export default function GameControls({
  onResign,
  onUndo,
  onFlip,
  onNewGame,
  canUndo = false,
  disabled = false,
}) {
  return (
    <div className="game-controls">
      <button onClick={onFlip} disabled={disabled} title="Flip Board">
        Flip Board
      </button>
      <button onClick={onUndo} disabled={disabled || !canUndo} title="Undo Move">
        Undo
      </button>
      <button onClick={onResign} disabled={disabled} title="Resign">
        Resign
      </button>
      <button onClick={onNewGame} title="New Game">
        New Game
      </button>
    </div>
  );
}