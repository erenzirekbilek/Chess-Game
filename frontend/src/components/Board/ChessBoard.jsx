import { useState, useCallback } from "react";
import { Chess } from "chess.js";
import { Chessboard } from "react-chessboard";

export default function ChessBoard({
  fen,
  onMove,
  boardOrientation = "white",
  showDots = true,
  boardWidth = 400,
}) {
  const [game, setGame] = useState(() => {
    if (fen) {
      const g = new Chess();
      g.load(fen);
      return g;
    }
    return new Chess();
  });

  const onPieceDrop = useCallback(
    (sourceSquare, targetSquare) => {
      try {
        const move = game.move({
          from: sourceSquare,
          to: targetSquare,
          promotion: "q",
        });

        if (move === null) return false;

        setGame(new Chess(game.fen()));

        if (onMove) {
          onMove(move);
        }

        return true;
      } catch (error) {
        return false;
      }
    },
    [game, onMove]
  );

  const getCustomPieces = useCallback(() => {
    const pieces = {};
    const pieceTypes = ["p", "n", "b", "r", "q", "k"];

    pieceTypes.forEach((type) => {
      pieces[`w${type}`] = require(`../assets/w${type}.png`).default;
      pieces[`b${type}`] = require(`../assets/b${type}.png`).default;
    });

    return pieces;
  }, []);

  return (
    <div className="chess-board-container">
      <Chessboard
        id="basic-board"
        position={fen || game.fen()}
        onPieceDrop={onPieceDrop}
        boardOrientation={boardOrientation}
        boardWidth={boardWidth}
        customBoardStyle={{
          borderRadius: "4px",
          boxShadow: "0 2px 10px rgba(0, 0, 0, 0.1)",
        }}
        customPieces={getCustomPieces()}
        showPromotionDialog={true}
      />
    </div>
  );
}