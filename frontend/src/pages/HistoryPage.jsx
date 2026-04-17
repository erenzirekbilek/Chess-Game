import { useState, useEffect } from "react";
import { getMyGames } from "../api/games";

export default function HistoryPage() {
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadGames();
  }, []);

  const loadGames = async () => {
    try {
      const data = await getMyGames();
      setGames(data);
    } catch (error) {
      console.error("Error loading games:", error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  const getResultClass = (result) => {
    if (result === "white_wins") return "win";
    if (result === "black_wins") return "lose";
    return "draw";
  };

  if (loading) {
    return <div className="history-page">Loading...</div>;
  }

  return (
    <div className="history-page">
      <h2>Game History</h2>
      {games.length === 0 ? (
        <p className="no-games">No games played yet. Start a game!</p>
      ) : (
        <div className="games-list">
          {games.map((game) => (
            <div key={game.id} className="game-card">
              <div className="game-info">
                <span className="game-type">{game.game_type}</span>
                <span className="game-date">{formatDate(game.created_at)}</span>
              </div>
              <div className="game-result">
                <span className={getResultClass(game.result)}>{game.result}</span>
              </div>
              <div className="game-moves">
                <span>{game.move_count} moves</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}