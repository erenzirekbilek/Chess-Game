import chess


def get_fen_parts(fen):
    parts = fen.split()
    if len(parts) < 6:
        return None
    return {
        "piece_placement": parts[0],
        "active_color": parts[1],
        "castling_rights": parts[2],
        "en_passant": parts[3],
        "halfmove_clock": parts[4],
        "fullmove_number": parts[5],
    }


def fen_to_array(fen):
    board = chess.Board(fen)
    array = []
    for rank in range(7, -1, -1):
        row = []
        for file in range(8):
            square = chess.square(file, rank)
            piece = board.piece_at(square)
            if piece:
                row.append(piece.symbol())
            else:
                row.append(".")
        array.append(row)
    return array


def get_legal_moves_uci(fen):
    board = chess.Board(fen)
    return [move.uci() for move in board.legal_moves]


def is_valid_fen(fen):
    try:
        board = chess.Board(fen)
        return True
    except:
        return False
