export default function PlayerInfo({ name, rating, color, isTurn, isKing }) {
  return (
    <div className={`player-info ${color} ${isTurn ? "active" : ""}`}>
      <div className="player-avatar">
        {isKing ? "♔" : "♙"}
      </div>
      <div className="player-details">
        <span className="player-name">{name}</span>
        <span className="player-rating">ELO: {rating || "1200"}</span>
      </div>
      {isTurn && <span className="turn-indicator">Your turn!</span>}
    </div>
  );
}