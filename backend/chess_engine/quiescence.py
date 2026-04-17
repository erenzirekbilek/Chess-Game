import chess
from .minimax import evaluate_position


def quiescence_search(
    board: chess.Board,
    alpha: float = float("-inf"),
    beta: float = float("inf"),
) -> int:
    stand_pat = evaluate_position(board)

    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    capture_moves = [move for move in board.legal_moves if board.is_capture(move)]

    if not capture_moves:
        return stand_pat

    capture_moves.sort(key=lambda m: move_order(m), reverse=True)

    for move in capture_moves:
        board.push(move)
        score = -quiescence_search(board, -beta, -alpha)
        board.pop()

        if score >= beta:
            return beta
        if score > alpha:
            alpha = score

    return alpha


def move_order(move: chess.Move) -> int:
    score = 0
    captured = board.piece_at(move.to_square) if board else None

    if captured:
        piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 300,
            chess.BISHOP: 300,
            chess.ROOK: 500,
            chess.QUEEN: 900,
        }
        captured_value = piece_values.get(captured.piece_type, 0)
        moving_piece = board.piece_at(move.from_square) if board else None
        moving_value = (
            piece_values.get(moving_piece.piece_type, 0) if moving_piece else 0
        )
        score = captured_value - moving_value

    return score


board = None


def see(board: chess.Board, square: chess.Square) -> int:
    piece = board.piece_at(square)
    if not piece:
        return 0

    piece_values = {
        chess.PAWN: 100,
        chess.KNIGHT: 300,
        chess.BISHOP: 300,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 10000,
    }

    return piece_values.get(piece.piece_type, 0)


def see_sign(board: chess.Board, move: chess.Move) -> bool:
    if board.is_en_passant(move):
        return True

    from_piece = board.piece_at(move.from_square)
    to_piece = board.piece_at(move.to_square)

    if not from_piece:
        return False

    if to_piece:
        if to_piece.color == from_piece.color:
            return False
        return see(board, move.to_square) <= see(board, move.from_square)

    if from_piece.piece_type == chess.PAWN:
        if chess.square_rank(move.to_square) in [0, 7]:
            return True
        return chess.square_file(move.from_square) != chess.square_file(move.to_square)

    return True


def quiescence_with_see(
    board: chess.Board,
    alpha: float = float("-inf"),
    beta: float = float("inf"),
) -> int:
    stand_pat = evaluate_position(board)

    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    capture_moves = [move for move in board.legal_moves if board.is_capture(move)]
    capture_moves = [m for m in capture_moves if see_sign(board, m)]

    if not capture_moves:
        return stand_pat

    capture_moves.sort(key=lambda m: capture_score(board, m), reverse=True)

    for move in capture_moves:
        board.push(move)
        score = -quiescence_with_see(board, -beta, -alpha)
        board.pop()

        if score >= beta:
            return beta
        if score > alpha:
            alpha = score

    return alpha


def capture_score(board: chess.Board, move: chess.Move) -> int:
    to_piece = board.piece_at(move.to_square)
    from_piece = board.piece_at(move.from_square)

    if not from_piece:
        return 0

    piece_values = {
        chess.PAWN: 100,
        chess.KNIGHT: 300,
        chess.BISHOP: 300,
        chess.ROOK: 500,
        chess.QUEEN: 900,
    }

    from_value = piece_values.get(from_piece.piece_type, 0)
    to_value = piece_values.get(to_piece.piece_type, 0) if to_piece else 0

    return to_value - from_value


def search_with_quiescence(
    board: chess.Board,
    depth: int,
    alpha: float = float("-inf"),
    beta: float = float("inf"),
) -> int:
    if depth == 0 or board.is_game_over():
        return quiescence_with_see(board, alpha, beta)

    if board.turn == chess.WHITE:
        max_eval = float("-inf")
        for move in board.legal_moves:
            board.push(move)
            eval_score = -search_with_quiescence(board, depth - 1, -beta, -alpha)
            board.pop()

            if eval_score > max_eval:
                max_eval = eval_score
            if max_eval > alpha:
                alpha = max_eval
            if alpha >= beta:
                return beta

        return max_eval
    else:
        min_eval = float("inf")
        for move in board.legal_moves:
            board.push(move)
            eval_score = -search_with_quiescence(board, depth - 1, -beta, -alpha)
            board.pop()

            if eval_score < min_eval:
                min_eval = eval_score
            if min_eval < beta:
                beta = min_eval
            if alpha >= beta:
                return alpha

        return min_eval
