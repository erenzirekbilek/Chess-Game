export default function CapturedPieces({ pieces = [] }) {
  const pieceSymbols = {
    p: "♟", n: "♞", b: "♝", r: "♜", q: "♛", k: "♚",
  };

  return (
    <div className="captured-pieces">
      <h4>Captured</h4>
      <div className="pieces-row">
        {pieces.map((piece, index) => (
          <span key={index} className={`piece ${piece.color}`}>
            {pieceSymbols[piece.type]}
          </span>
        ))}
      </div>
    </div>
  );
}