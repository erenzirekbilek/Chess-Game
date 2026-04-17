export default function GameAnalysis({ moves = [] }) {
  const getOpeningMove = () => {
    if (moves.length < 4) return null;
    const opening = moves.slice(0, 4).map((m) => m.san || m).join(" ");
    return opening;
  };

  const getGameSummary = () => {
    if (moves.length === 0) return "No moves made";
    const totalMoves = moves.length;
    const whiteMoves = Math.ceil(totalMoves / 2);
    const blackMoves = Math.floor(totalMoves / 2);
    return `${totalMoves} moves (White: ${whiteMoves}, Black: ${blackMoves})`;
  };

  return (
    <div className="game-analysis">
      <h3>Game Analysis</h3>
      <div className="analysis-item">
        <span className="label">Opening:</span>
        <span className="value">{getOpeningMove() || "Unknown"}</span>
      </div>
      <div className="analysis-item">
        <span className="label">Duration:</span>
        <span className="value">{getGameSummary()}</span>
      </div>
      <div className="analysis-item">
        <span className="label">Move count:</span>
        <span className="value">{moves.length}</span>
      </div>
    </div>
  );
}