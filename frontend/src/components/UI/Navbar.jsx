export default function Navbar({ currentPage, onNavigate }) {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <span className="logo">♟</span>
        <h1>Chess Game</h1>
      </div>
      <div className="navbar-links">
        <button
          className={currentPage === "home" ? "active" : ""}
          onClick={() => onNavigate("home")}
        >
          Home
        </button>
        <button
          className={currentPage === "game" ? "active" : ""}
          onClick={() => onNavigate("game")}
        >
          Play vs AI
        </button>
        <button
          className={currentPage === "online" ? "active" : ""}
          onClick={() => onNavigate("online")}
        >
          Online
        </button>
        <button
          className={currentPage === "history" ? "active" : ""}
          onClick={() => onNavigate("history")}
        >
          History
        </button>
      </div>
    </nav>
  );
}