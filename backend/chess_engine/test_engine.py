import chess
from engine import create_engine, ChessEngine, Difficulty


def test_engine():
    board = chess.Board()
    engine = create_engine(difficulty="medium")

    print("Testing Chess Engine...")
    print(f"Difficulty: {engine.difficulty.name}")
    print(f"Depth: {engine.depth}")

    move = engine.get_best_move(board)
    print(f"Best move from starting position: {move}")

    count = 0
    while not board.is_game_over() and count < 10:
        player_move = engine.get_best_move(board)
        if player_move:
            board.push(player_move)
            print(f"Move {count + 1}: {player_move}")

            if not board.is_game_over():
                ai_move = engine.get_best_move(board)
                if ai_move:
                    board.push(ai_move)
                    print(f"AI move: {ai_move}")
        count += 1

    print(f"\nGame over: {board.is_game_over()}")
    print(f"Result: {board.outcome()}")


if __name__ == "__main__":
    test_engine()
