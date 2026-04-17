import { useState } from "react";
import GamePage from "./pages/GamePage";
import "./App.css";

function App() {
  const [currentPage, setCurrentPage] = useState("game");

  return (
    <div className="app">
      <nav className="navbar">
        <h1>Chess Game</h1>
        <div className="nav-links">
          <button onClick={() => setCurrentPage("game")}>Play vs AI</button>
          <button onClick={() => setCurrentPage("online")}>Online</button>
          <button onClick={() => setCurrentPage("history")}>History</button>
        </div>
      </nav>

      <main className="main-content">
        {currentPage === "game" && <GamePage />}
        {currentPage === "online" && <div className="online-page">Online multiplayer coming soon!</div>}
        {currentPage === "history" && <div className="history-page">Game history coming soon!</div>}
      </main>
    </div>
  );
}

export default App;