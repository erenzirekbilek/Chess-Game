import { useState } from "react";
import { AuthProvider } from "./context/AuthContext";
import { ThemeProvider } from "./context/ThemeContext";
import Navbar from "./components/UI/Navbar";
import ThemeToggle from "./components/UI/ThemeToggle";
import HomePage from "./pages/HomePage";
import GamePage from "./pages/GamePage";
import HistoryPage from "./pages/HistoryPage";
import ProfilePage from "./pages/ProfilePage";
import LobbyPage from "./pages/LobbyPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import "./index.css";

function App() {
  const [currentPage, setCurrentPage] = useState("home");
  const [gameStarted, setGameStarted] = useState(false);
  const [difficulty, setDifficulty] = useState("medium");

  const handleStartGame = (type, diff) => {
    if (type === "vs_ai") {
      setDifficulty(diff || "medium");
      setCurrentPage("game");
      setGameStarted(true);
    } else {
      setCurrentPage("online");
    }
  };

  const renderPage = () => {
    switch (currentPage) {
      case "home":
        return <HomePage onStartGame={handleStartGame} />;
      case "game":
        return <GamePage difficulty={difficulty} key={gameStarted ? "new" : "existing"} />;
      case "history":
        return <HistoryPage />;
      case "profile":
        return <ProfilePage user={null} stats={null} />;
      case "online":
        return <LobbyPage onGameStart={(gameId) => console.log("Game:", gameId)} />;
      case "login":
        return <LoginPage onLogin={() => setCurrentPage("home")} onGoToRegister={() => setCurrentPage("register")} />;
      case "register":
        return <RegisterPage onRegister={() => setCurrentPage("home")} onGoToLogin={() => setCurrentPage("login")} />;
      default:
        return <HomePage onStartGame={handleStartGame} />;
    }
  };

  return (
    <ThemeProvider>
      <AuthProvider>
        <div className="app">
          <nav className="navbar">
            <div className="navbar-brand" onClick={() => setCurrentPage("home")}>
              <span className="logo">♟</span>
              <h1>Chess Game</h1>
            </div>
            <div className="navbar-links">
              <button className={currentPage === "home" ? "active" : ""} onClick={() => setCurrentPage("home")}>
                Home
              </button>
              <button className={currentPage === "game" ? "active" : ""} onClick={() => setCurrentPage("game")}>
                Play vs AI
              </button>
              <button className={currentPage === "online" ? "active" : ""} onClick={() => setCurrentPage("online")}>
                Online
              </button>
              <button className={currentPage === "history" ? "active" : ""} onClick={() => setCurrentPage("history")}>
                History
              </button>
            </div>
            <div className="navbar-actions">
              <ThemeToggle />
            </div>
          </nav>
          <main className="main-content">{renderPage()}</main>
        </div>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;