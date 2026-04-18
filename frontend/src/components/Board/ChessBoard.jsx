import { useCallback, useEffect, useRef } from "react";
import { Chessboard } from "react-chessboard";

export default function ChessBoard({
  fen,
  onMove,
  boardOrientation = "white",
  boardWidth = 450,
  arePiecesDraggable = true,
}) {
  const onPieceDrop = useCallback(
    (sourceSquare, targetSquare) => {
      if (!arePiecesDraggable) return false;
      
      if (onMove) {
        onMove({
          from: sourceSquare,
          to: targetSquare,
        });
      }

      return true;
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
        position={fen}
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