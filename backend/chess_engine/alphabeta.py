import chess
from typing import Optional
from .minimax import evaluate_position


def alpha_beta_search(
    board: chess.Board,
    depth: int,
    alpha: float = float("-inf"),
    beta: float = float("inf"),
    maximizing: bool = True,
) -> tuple[Optional[chess.Move], int]:
    if depth == 0 or board.is_game_over():
        return None, evaluate_position(board)

    best_move = None
    legal_moves = list(board.legal_moves)

    if not legal_moves:
        return None, evaluate_position(board)

    if maximizing:
        max_eval = float("-inf")
        for move in legal_moves:
            board.push(move)
            _, eval_score = alpha_beta_search(board, depth - 1, alpha, beta, False)
            board.pop()

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break

        return best_move, max_eval
    else:
        min_eval = float("inf")
        for move in legal_moves:
            board.push(move)
            _, eval_score = alpha_beta_search(board, depth - 1, alpha, beta, True)
            board.pop()

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move

            beta = min(beta, eval_score)
            if beta <= alpha:
                break

        return best_move, min_eval


def iterative_deepening(
    board: chess.Board, max_depth: int = 4
) -> tuple[Optional[chess.Move], int]:
    best_move = None
    score = 0

    for depth in range(1, max_depth + 1):
        best_move, score = alpha_beta_search(
            board, depth, maximizing=board.turn == chess.WHITE
        )

    return best_move, score


def fuzzy_search(
    board: chess.Board,
    depth: int,
    alpha: float = float("-inf"),
    beta: float = float("inf"),
) -> tuple[Optional[chess.Move], int]:
    if depth == 0:
        return None, evaluate_position(board)

    moves = list(board.legal_moves)
    if not moves:
        return None, evaluate_position(board)

    best_move = moves[0]

    if board.turn == chess.WHITE:
        max_eval = float("-inf")
        for move in moves:
            board.push(move)
            _, eval_score = fuzzy_search(board, depth - 1, alpha, beta)
            board.pop()

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break

        return best_move, max_eval
    else:
        min_eval = float("inf")
        for move in moves:
            board.push(move)
            _, eval_score = fuzzy_search(board, depth - 1, alpha, beta)
            board.pop()

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move

            beta = min(beta, eval_score)
            if beta <= alpha:
                break

        return best_move, min_eval


def aspiration_window(
    board: chess.Board, depth: int, alpha: float, beta: float
) -> tuple[Optional[chess.Move], int]:
    best_move = None
    score = 0

    while True:
        if board.turn == chess.WHITE:
            best_move, score = alpha_beta_search(board, depth, alpha, beta, True)
        else:
            best_move, score = alpha_beta_search(board, depth, alpha, beta, False)

        if score <= alpha or score >= beta or score == 0:
            return best_move, score

        if score <= alpha:
            alpha = float("-inf")
            beta = score
        elif score >= beta:
            beta = float("inf")

    return best_move, score
