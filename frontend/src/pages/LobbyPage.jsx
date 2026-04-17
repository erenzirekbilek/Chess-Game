import { useState } from "react";
import { useWebSocket } from "../hooks/useWebSocket";
import MatchmakingSpinner from "../components/Lobby/MatchmakingSpinner";

export default function LobbyPage({ onGameStart }) {
  const [status, setStatus] = useState("idle");
  const wsUrl = "ws://localhost:8000/ws/lobby/";
  const { isConnected, send, lastMessage } = useWebSocket(wsUrl);

  const joinQueue = () => {
    setStatus("searching");
    send({ action: "join_queue" });
  };

  const leaveQueue = () => {
    setStatus("idle");
    send({ action: "leave_queue" });
  };

  if (lastMessage?.type === "game_ready") {
    onGameStart(lastMessage.game_id);
  }

  return (
    <div className="lobby-page">
      <h1>Online Lobby</h1>

      <div className="connection-status">
        <span className={isConnected ? "connected" : "disconnected"}>
          {isConnected ? "Connected" : "Disconnected"}
        </span>
      </div>

      {status === "searching" ? (
        <MatchmakingSpinner onCancel={leaveQueue} />
      ) : (
        <div className="lobby-actions">
          <div className="lobby-card" onClick={joinQueue}>
            <h2>Find Match</h2>
            <p>Search for a random opponent</p>
          </div>
          <div className="lobby-card">
            <h2>Create Private</h2>
            <p>Create a private room</p>
          </div>
        </div>
      )}

      <div className="online-players">
        <h3>Online Players</h3>
        <p className="player-count">{Math.floor(Math.random() * 50) + 10} players online</p>
      </div>
    </div>
  );
}