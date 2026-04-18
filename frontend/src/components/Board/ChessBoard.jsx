import { useCallback, useEffect, useRef, useState } from "react";
import { Chess } from "chess.js";
import { Chessboard } from "react-chessboard";

export default function ChessBoard({
  fen,
  onMove,
  boardOrientation = "white",
  boardWidth = 450,
  arePiecesDraggable = true,
}) {
  const gameRef = useRef(new Chess());
  const [position, setPosition] = useState("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1");

  useEffect(() => {
    if (fen) {
      try {
        gameRef.current.load(fen);
        setPosition(fen);
      } catch (e) {
        console.error("Invalid FEN:", e);
      }
    }
  }, [fen]);

  const onPieceDrop = useCallback(
    (sourceSquare, targetSquare) => {
      if (!arePiecesDraggable) return false;
      
      try {
        const game = gameRef.current;
        
        const move = game.move({
          from: sourceSquare,
          to: targetSquare,
          promotion: "q",
        });

        if (move === null) {
          return false;
        }

        setPosition(game.fen());

        if (onMove) {
          onMove({
            from: sourceSquare,
            to: targetSquare,
            san: move.san,
          });
        }

        return true;
      } catch (error) {
        console.error("Move error:", error);
        return false;
      }
    },
    [onMove, arePiecesDraggable]
  );

  return (
    <div style={{ 
      display: "flex", 
      justifyContent: "center", 
      padding: "20px",
      background: "#2d2d2d",
      borderRadius: "12px",
    }}>
      <Chessboard
        id="basic-board"
        position={position}
        onPieceDrop={onPieceDrop}
        boardOrientation={boardOrientation}
        boardWidth={boardWidth}
        arePiecesDraggable={arePiecesDraggable}
        customBoardStyle={{
          borderRadius: "8px",
          boxShadow: "0 8px 32px rgba(0, 0, 0, 0.4)",
        }}
        customDarkSquareStyle={{ backgroundColor: "#769656" }}
        customLightSquareStyle={{ backgroundColor: "#eeeed2" }}
      />
    </div>
  );
}