import { useState, useEffect, useCallback } from "react";
import { Chess } from "chess.js";
import ChessBoard from "../components/Board/ChessBoard";
import { createGame, getGame, makeMove, resignGame } from "../api/games";

export default function GamePage() {
  const [gameId, setGameId] = useState(null);
  const [fen, setFen] = useState(null);
  const [currentTurn, setCurrentTurn] = useState("white");
  const [gameStatus, setGameStatus] = useState(null);
  const [difficulty, setDifficulty] = useState("medium");
  const [isThinking, setIsThinking] = useState(false);
  const [gameOver, setGameOver] = useState(false);
  const [result, setResult] = useState(null);
  const [boardOrientation, setBoardOrientation] = useState("white");

  const startNewGame = async (diff = "medium") => {
    try {
      setDifficulty(diff);
      const game = await createGame("vs_ai", diff, "black");
      setGameId(game.id);
      setFen(game.fen);
      setCurrentTurn(game.current_turn);
      setGameStatus(game.status);
      setGameOver(false);
      setResult(null);
    } catch (error) {
      console.error("Error creating game:", error);
    }
  };

  const handleMove = async (move) => {
    if (!gameId || isThinking || gameOver) return;

    try {
      const response = await makeMove(gameId, move.to);

      if (response.fen) {
        setFen(response.fen);
        setCurrentTurn(response.turn);

        if (response.is_checkmate) {
          setGameOver(true);
          setResult(response.is_checkmate ? "You Win!" : "You Lose!");
        } else if (response.is_stalemate) {
          setGameOver(true);
          setResult("Draw!");
        }
      }

      if (response.ai_move) {
        setIsThinking(true);
        setTimeout(() => {
          setFen(response.ai_fen);
          setCurrentTurn(response.turn);
          setIsThinking(false);

          if (response.is_checkmate) {
            setGameOver(true);
            setResult("You Lose!");
          }
        }, 500);
      }
    } catch (error) {
      console.error("Error making move:", error);
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
    <div className="game-page">
      <div className="game-header">
        <h1>Chess vs AI</h1>
        <div className="difficulty-selector">
          <label>Difficulty: </label>
          <select
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
            disabled={!!gameId}
          >
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
            <option value="expert">Expert</option>
          </select>
        </div>
      </div>

      {isThinking && (
        <div className="thinking-indicator">AI is thinking...</div>
      )}

      <div className="game-container">
        <ChessBoard
          fen={fen}
          onMove={handleMove}
          boardOrientation={boardOrientation}
        />
      </div>

      <div className="game-controls">
        <button onClick={handleFlipBoard}>Flip Board</button>
        <button onClick={handleResign} disabled={gameOver}>
          Resign
        </button>
        <button onClick={() => startNewGame(difficulty)}>New Game</button>
      </div>

      {gameOver && (
        <div className="game-over-modal">
          <div className="modal-content">
            <h2>Game Over</h2>
            <p className="result">{result}</p>
            <button onClick={() => startNewGame(difficulty)}>Play Again</button>
          </div>
        </div>
      )}

      <div className="game-info">
        <p>Turn: {currentTurn}</p>
        <p>Status: {gameStatus}</p>
      </div>
    </div>
  );
}