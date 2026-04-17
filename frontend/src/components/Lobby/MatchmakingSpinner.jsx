export default function MatchmakingSpinner({ onCancel }) {
  return (
    <div className="matchmaking-overlay">
      <div className="matchmaking-content">
        <div className="spinner-large"></div>
        <h2>Finding opponent...</h2>
        <p>Please wait while we match you with an opponent</p>
        <button onClick={onCancel}>Cancel</button>
      </div>
    </div>
  );
}