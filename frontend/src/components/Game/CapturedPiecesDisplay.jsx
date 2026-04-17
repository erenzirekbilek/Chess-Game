export default function CapturedPiecesDisplay({ captured = [] }) {
  const getPieceSymbol = (piece) => {
    const symbols = { p: "♟", n: "♞", b: "♝", r: "♜", q: "♛", k: "♚" };
    return symbols[piece.type] || "";
  };

  const valueMap = { p: 1, n: 3, b: 3, r: 5, q: 9, k: 0 };

  const whitePieces = captured.filter((p) => p.color === "white");
  const blackPieces = captured.filter((p) => p.color === "black");

  const whiteValue = whitePieces.reduce((sum, p) => sum + (valueMap[p.type] || 0), 0);
  const blackValue = blackPieces.reduce((sum, p) => sum + (valueMap[p.type] || 0), 0);

  return (
    <div className="captured-pieces-display">
      <div className="captured-row white">
        <span className="player-label">White</span>
        <div className="pieces">
          {whitePieces.map((p, i) => (
            <span key={i} className="piece">{getPieceSymbol(p)}</span>
          ))}
        </div>
        <span className="material-diff">+{whiteValue - blackValue}</span>
      </div>
      <div className="captured-row black">
        <span className="player-label">Black</span>
        <div className="pieces">
          {blackPieces.map((p, i) => (
            <span key={i} className="piece">{getPieceSymbol(p)}</span>
          ))}
        </div>
        <span className="material-diff">+{blackValue - whiteValue}</span>
      </div>
    </div>
  );
}