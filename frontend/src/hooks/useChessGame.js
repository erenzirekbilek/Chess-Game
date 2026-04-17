import { useState, useCallback, useEffect } from "react";
import { Chess } from "chess.js";

export function useChessGame(initialPosition) {
  const [game, setGame] = useState(() => {
    const g = new Chess();
    if (initialPosition) {
      g.load(initialPosition);
    }
    return g;
  });

  const [position, setPosition] = useState(game.fen());
  const [history, setHistory] = useState([]);
  const [turn, setTurn] = useState("white");
  const [inCheck, setInCheck] = useState(false);
  const [isGameOver, setIsGameOver] = useState(false);
  const [result, setResult] = useState(null);

  const updateState = useCallback(() => {
    setPosition(game.fen());
    setTurn(game.turn() === "w" ? "white" : "black");
    setInCheck(game.inCheck());
    setIsGameOver(game.isGameOver());

    if (game.isGameOver()) {
      if (game.isCheckmate()) {
        setResult(game.turn() === "w" ? "Black wins!" : "White wins!");
      } else if (game.isStalemate()) {
        setResult("Draw!");
      } else if (game.isThreefoldRepetition()) {
        setResult("Draw by threefold repetition!");
      } else if (game.isInsufficientMaterial()) {
        setResult("Draw by insufficient material!");
      } else {
        setResult("Game over!");
      }
    }

    setHistory(game.history({ verbose: true }));
  }, [game]);

  useEffect(() => {
    updateState();
  }, [initialPosition]);

  const makeMove = useCallback(
    (source, target, promotion) => {
      try {
        const move = game.move({
          from: source,
          to: target,
          promotion: promotion || "q",
        });

        if (move) {
          updateState();
          return move;
        }
        return null;
      } catch (error) {
        console.error("Move error:", error);
        return null;
      }
    },
    [game, updateState]
  );

  const undo = useCallback(() => {
    const move = game.undo();
    if (move) {
      updateState();
      return move;
    }
    return null;
  }, [game, updateState]);

  const reset = useCallback(() => {
    game.reset();
    updateState();
  }, [game, updateState]);

  const loadPgn = useCallback(
    (pgn) => {
      try {
        game.load_pgn(pgn);
        updateState();
      } catch (error) {
        console.error("PGN load error:", error);
      }
    },
    [game, updateState]
  );

  const getSan = useCallback((move) => {
    return game.san(move);
  }, [game]);

  return {
    game,
    position,
    history,
    turn,
    inCheck,
    isGameOver,
    result,
    makeMove,
    undo,
    reset,
    loadPgn,
    getSan,
  };
}