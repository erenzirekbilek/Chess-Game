export default function PromotionDialog({ isOpen, onSelect, onClose }) {
  if (!isOpen) return null;

  const pieces = [
    { type: "q", symbol: "♛", label: "Queen" },
    { type: "r", symbol: "♜", label: "Rook" },
    { type: "b", symbol: "♝", label: "Bishop" },
    { type: "n", symbol: "♞", label: "Knight" },
  ];

  return (
    <div className="promotion-dialog">
      <div className="dialog-overlay" onClick={onClose}></div>
      <div className="dialog-content">
        <h3>Promote Pawn</h3>
        <div className="piece-options">
          {pieces.map((piece) => (
            <button key={piece.type} onClick={() => onSelect(piece.type)}>
              <span className="piece-symbol">{piece.symbol}</span>
              <span className="piece-label">{piece.label}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}