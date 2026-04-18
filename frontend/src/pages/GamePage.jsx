import { useState, useEffect, useCallback, useRef } from "react";
import { Chess } from "chess.js";
import ChessBoard from "../components/Board/ChessBoard";
import { createGame, makeMove, resignGame } from "../api/games";

const GAME_TIME = 10 * 60;

export default function GamePage() {
  const [gameId, setGameId] = useState(null);
  const [fen, setFen] = useState("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1");
  const [currentTurn, setCurrentTurn] = useState("white");
  const [gameStatus, setGameStatus] = useState(null);
  const [difficulty, setDifficulty] = useState("medium");
  const [isThinking, setIsThinking] = useState(false);
  const [gameOver, setGameOver] = useState(false);
  const [result, setResult] = useState(null);
  const [boardOrientation, setBoardOrientation] = useState("white");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [playerColor] = useState("white");
  const [whiteTime, setWhiteTime] = useState(GAME_TIME);
  const [blackTime, setBlackTime] = useState(GAME_TIME);
  const [lastMove, setLastMove] = useState(null);
  const [moveHistory, setMoveHistory] = useState([]);
  
  const timerRef = useRef(null);

  useEffect(() => {
    if (!gameOver && gameId) {
      timerRef.current = setInterval(() => {
        if (currentTurn === "white") {
          setWhiteTime(prev => Math.max(0, prev - 1));
        } else {
          setBlackTime(prev => Math.max(0, prev - 1));
        }
      }, 1000);
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [currentTurn, gameOver, gameId]);

  useEffect(() => {
    if (whiteTime === 0 || blackTime === 0) {
      setGameOver(true);
      setResult(whiteTime === 0 ? "Time's up! Black wins!" : "Time's up! White wins!");
    }
  }, [whiteTime, blackTime]);

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, "0")}`;
  };

  const startNewGame = async (diff = "medium") => {
    setLoading(true);
    setError(null);
    setGameOver(false);
    setResult(null);
    setWhiteTime(GAME_TIME);
    setBlackTime(GAME_TIME);
    setMoveHistory([]);
    setLastMove(null);
    
    try {
      const game = await createGame("vs_ai", diff, "black");
      setGameId(game.id);
      setFen(game.fen);
      setCurrentTurn(game.current_turn);
      setGameStatus(game.status);
    } catch (err) {
      console.error("Error creating game:", err);
      setError("Failed to connect to server. Playing offline mode.");
      setGameId(null);
      setFen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1");
      setCurrentTurn("white");
    } finally {
      setLoading(false);
    }
  };

  const handleMove = async (move) => {
    if (isThinking || gameOver) return;
    
    setIsThinking(true);
    setLastMove(move);

    try {
      if (gameId) {
        const uci = move.from + move.to;
        const response = await makeMove(gameId, uci);

        if (response.fen) {
          setFen(response.fen);
          const newTurn = response.turn || (currentTurn === "white" ? "black" : "white");
          setCurrentTurn(newTurn);
          setMoveHistory(prev => [...prev, move.san]);

          if (response.is_checkmate) {
            setGameOver(true);
            setResult("♛ Checkmate! You Win!");
          } else if (response.is_stalemate) {
            setGameOver(true);
            setResult("Draw by Stalemate!");
          } else if (response.is_check) {
            console.log("Check!");
          }
        }

        if (response.ai_move) {
          setTimeout(() => {
            setFen(response.ai_fen);
            setCurrentTurn(response.turn || "white");
            setMoveHistory(prev => [...prev, response.ai_move]);
            
            if (response.is_checkmate) {
              setGameOver(true);
              setResult("♛ Checkmate! You Lose!");
            }
            setIsThinking(false);
          }, 600);
        } else {
          setIsThinking(false);
        }
      } else {
        setCurrentTurn(currentTurn === "white" ? "black" : "white");
        setIsThinking(false);
      }
    } catch (err) {
      console.error("Error making move:", err);
      setCurrentTurn(currentTurn === "white" ? "black" : "white");
      setIsThinking(false);
    }
  };

  const handleResign = async () => {
    if (!gameId) return;
    try {
      await resignGame(gameId);
      setGameOver(true);
      setResult("You Resigned!");
    } catch (error) {
      console.error("Error resigning:", error);
    }
  };

  const handleFlipBoard = () => {
    setBoardOrientation(boardOrientation === "white" ? "black" : "white");
  };

  useEffect(() => {
    startNewGame();
  }, []);

  return (
    <div style={{ 
      minHeight: "100vh", 
      background: "linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)",
      padding: "20px",
    }}>
      <div style={{ maxWidth: "1200px", margin: "0 auto" }}>
        <div style={{ 
          display: "flex", 
          justifyContent: "space-between", 
          alignItems: "center",
          marginBottom: "20px",
          color: "#fff"
        }}>
          <h1 style={{ margin: 0, fontSize: "2rem" }}>♟ Chess vs AI</h1>
          <div style={{ display: "flex", gap: "15px", alignItems: "center" }}>
            <label style={{ color: "#aaa" }}>Difficulty:</label>
            <select
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value)}
              disabled={!!gameId || gameOver}
              style={{
                padding: "8px 16px",
                borderRadius: "8px",
                border: "none",
                background: "#2d2d2d",
                color: "#fff",
                fontSize: "1rem",
                cursor: "pointer",
              }}
            >
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
              <option value="expert">Expert</option>
            </select>
          </div>
        </div>

        <div style={{ 
          display: "grid", 
          gridTemplateColumns: "1fr 2fr 1fr", 
          gap: "20px",
          alignItems: "start",
        }}>
          <div style={{ 
            background: "#1e1e2e", 
            borderRadius: "16px", 
            padding: "20px",
            color: "#fff",
          }}>
            <h3 style={{ marginTop: 0 }}>♔ Player</h3>
            <div style={{ 
              padding: "15px", 
              borderRadius: "12px",
              background: currentTurn === "white" && !gameOver ? "#3d5a3d" : "#2d2d2d",
              border: currentTurn === "white" && !gameOver ? "2px solid #4caf50" : "2px solid transparent",
              marginBottom: "15px",
            }}>
              <div style={{ fontSize: "1.2rem", fontWeight: "bold" }}>You (White)</div>
              <div style={{ fontSize: "2rem", fontFamily: "monospace", color: "#4caf50" }}>
                {formatTime(whiteTime)}
              </div>
            </div>
            
            <h3>♚ Computer</h3>
            <div style={{ 
              padding: "15px", 
              borderRadius: "12px",
              background: currentTurn === "black" && !gameOver ? "#3d5a3d" : "#2d2d2d",
              border: currentTurn === "black" && !gameOver ? "2px solid #4caf50" : "2px solid transparent",
            }}>
              <div style={{ fontSize: "1.2rem", fontWeight: "bold" }}>AI ({difficulty})</div>
              <div style={{ fontSize: "2rem", fontFamily: "monospace", color: "#f44336" }}>
                {formatTime(blackTime)}
              </div>
            </div>
          </div>

          <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
            {loading && (
              <div style={{ 
                color: "#fff", 
                fontSize: "1.2rem",
                marginBottom: "10px",
              }}>
                ⏳ Starting game...
              </div>
            )}
            {error && (
              <div style={{ 
                color: "#ff6b6b", 
                marginBottom: "10px",
                padding: "10px",
                background: "rgba(255,107,107,0.1)",
                borderRadius: "8px",
              }}>
                {error}
              </div>
            )}
            {isThinking && !gameOver && (
              <div style={{ 
                color: "#ffd93d", 
                fontSize: "1.2rem",
                marginBottom: "10px",
                animation: "pulse 1s infinite",
              }}>
                🤖 AI is thinking...
              </div>
            )}
            {!gameOver && !loading && (
              <div style={{ 
                color: currentTurn === "white" ? "#fff" : "#ccc",
                fontSize: "1.1rem",
                marginBottom: "10px",
              }}>
                Turn: <span style={{ 
                  color: currentTurn === "white" ? "#fff" : "#f44336",
                  fontWeight: "bold",
                }}>
                  {currentTurn === "white" ? "♔ Your Turn" : "♚ AI's Turn"}
                </span>
              </div>
            )}

            <ChessBoard
              fen={fen}
              onMove={handleMove}
              boardOrientation={boardOrientation}
              arePiecesDraggable={!isThinking && !gameOver && currentTurn === "white"}
            />

            <div style={{ display: "flex", gap: "12px", marginTop: "20px" }}>
              <button 
                onClick={handleFlipBoard}
                style={{
                  padding: "12px 24px",
                  borderRadius: "8px",
                  border: "none",
                  background: "#4a4a6a",
                  color: "#fff",
                  cursor: "pointer",
                  fontSize: "1rem",
                  transition: "all 0.2s",
                }}
              >
                🔄 Flip Board
              </button>
              <button 
                onClick={() => startNewGame(difficulty)}
                style={{
                  padding: "12px 24px",
                  borderRadius: "8px",
                  border: "none",
                  background: "#4caf50",
                  color: "#fff",
                  cursor: "pointer",
                  fontSize: "1rem",
                  transition: "all 0.2s",
                }}
              >
                🆕 New Game
              </button>
              <button 
                onClick={handleResign} 
                disabled={gameOver || !gameId}
                style={{
                  padding: "12px 24px",
                  borderRadius: "8px",
                  border: "none",
                  background: gameOver || !gameId ? "#555" : "#f44336",
                  color: "#fff",
                  cursor: gameOver || !gameId ? "not-allowed" : "pointer",
                  fontSize: "1rem",
                  transition: "all 0.2s",
                  opacity: gameOver || !gameId ? 0.5 : 1,
                }}
              >
                🏳️ Resign
              </button>
            </div>
          </div>

          <div style={{ 
            background: "#1e1e2e", 
            borderRadius: "16px", 
            padding: "20px",
            color: "#fff",
            maxHeight: "500px",
            overflowY: "auto",
          }}>
            <h3 style={{ marginTop: 0 }}>📜 Move History</h3>
            {moveHistory.length === 0 ? (
              <p style={{ color: "#666" }}>No moves yet</p>
            ) : (
              <div style={{ display: "flex", flexDirection: "column", gap: "5px" }}>
                {moveHistory.map((move, index) => (
                  <div key={index} style={{ 
                    padding: "8px 12px", 
                    background: index % 2 === 0 ? "#2d2d2d" : "#3d3d3d",
                    borderRadius: "6px",
                    fontFamily: "monospace",
                  }}>
                    {Math.floor(index / 2) + 1}. {move}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {gameOver && (
          <div style={{
            position: "fixed",
            inset: 0,
            background: "rgba(0,0,0,0.8)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 1000,
          }}>
            <div style={{
              background: "linear-gradient(135deg, #1e1e2e 0%, #2d2d4a 100%)",
              padding: "40px",
              borderRadius: "20px",
              textAlign: "center",
              color: "#fff",
              boxShadow: "0 20px 60px rgba(0,0,0,0.5)",
            }}>
              <div style={{ fontSize: "4rem", marginBottom: "20px" }}>
                {result?.includes("Win") ? "🏆" : result?.includes("Lose") ? "😢" : "🤝"}
              </div>
              <h2 style={{ fontSize: "2rem", margin: "0 0 20px 0" }}>
                {result}
              </h2>
              <button 
                onClick={() => startNewGame(difficulty)}
                style={{
                  padding: "15px 40px",
                  borderRadius: "12px",
                  border: "none",
                  background: "linear-gradient(135deg, #4caf50 0%, #2e7d32 100%)",
                  color: "#fff",
                  cursor: "pointer",
                  fontSize: "1.2rem",
                  fontWeight: "bold",
                }}
              >
                Play Again
              </button>
            </div>
          </div>
        )}
      </div>
      
      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
      `}</style>
    </div>
  );
}