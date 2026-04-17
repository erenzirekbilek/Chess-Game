import { useState, useEffect, useCallback } from "react";
import { Chess } from "chess.js";

export function useGameInit(fen) {
  const [game, setGame] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    initializeGame();
  }, [fen]);

  const initializeGame = useCallback(() => {
    setLoading(true);
    try {
      const g = new Chess();
      if (fen) {
        const loaded = g.load(fen);
        if (!loaded) {
          throw new Error("Invalid FEN string");
        }
      }
      setGame(g);
      setError(null);
    } catch (err) {
      setError(err.message);
      setGame(new Chess());
    } finally {
      setLoading(false);
    }
  }, [fen]);

  return { game, loading, error, initializeGame };
}