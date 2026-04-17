export default function ProfilePage({ user, stats }) {
  return (
    <div className="profile-page">
      <div className="profile-header">
        <div className="avatar">♟</div>
        <h2>{user?.username || "Guest"}</h2>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <span className="stat-value">{stats?.games_played || 0}</span>
          <span className="stat-label">Games Played</span>
        </div>
        <div className="stat-card wins">
          <span className="stat-value">{stats?.wins || 0}</span>
          <span className="stat-label">Wins</span>
        </div>
        <div className="stat-card losses">
          <span className="stat-value">{stats?.losses || 0}</span>
          <span className="stat-label">Losses</span>
        </div>
        <div className="stat-card draws">
          <span className="stat-value">{stats?.draws || 0}</span>
          <span className="stat-label">Draws</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{stats?.elo_rating || 1200}</span>
          <span className="stat-label">ELO Rating</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{stats?.win_rate?.toFixed(1) || 0}%</span>
          <span className="stat-label">Win Rate</span>
        </div>
      </div>
    </div>
  );
}