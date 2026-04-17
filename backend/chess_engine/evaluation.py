import chess
import numpy as np
from typing import Optional


PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000,
}

PAWN_TABLE = np.array(
    [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [0, 0, 0, 20, 20, 0, 0, 0],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    dtype=np.int32,
)

KNIGHT_TABLE = np.array(
    [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-30, 5, 15, 20, 20, 15, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50],
    ],
    dtype=np.int32,
)

BISHOP_TABLE = np.array(
    [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 5, 5, 10, 10, 5, 5, -10],
        [-10, 0, 10, 10, 10, 10, 0, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20],
    ],
    dtype=np.int32,
)

ROOK_TABLE = np.array(
    [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 10, 10, 10, 10, 10, 10, 5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [0, 0, 0, 5, 5, 0, 0, 0],
    ],
    dtype=np.int32,
)

QUEEN_TABLE = np.array(
    [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-10, 5, 5, 5, 5, 5, 0, -10],
        [-10, 0, 5, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20],
    ],
    dtype=np.int32,
)

KING_TABLE = np.array(
    [
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [20, 20, 0, 0, 0, 0, 20, 20],
        [20, 30, 10, 0, 0, 10, 30, 20],
    ],
    dtype=np.int32,
)

TABLES = {
    chess.PAWN: PAWN_TABLE,
    chess.KNIGHT: KNIGHT_TABLE,
    chess.BISHOP: BISHOP_TABLE,
    chess.ROOK: ROOK_TABLE,
    chess.QUEEN: QUEEN_TABLE,
    chess.KING: KING_TABLE,
}


def evaluate_material(board: chess.Board) -> int:
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = PIECE_VALUES[piece.piece_type]
            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value
    return score


def evaluate_position(board: chess.Board) -> int:
    if board.is_checkmate():
        if board.turn:
            return -9999
        return 9999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    score = evaluate_material(board)

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and piece.piece_type in TABLES:
            rank = chess.rank_of(square)
            file = chess.file_of(square)
            table = TABLES[piece.piece_type]

            if piece.color == chess.WHITE:
                score += table[rank][file]
            else:
                score -= table[7 - rank][file]

    return score if board.turn == chess.WHITE else -score


def evaluate_board(board: chess.Board) -> int:
    return evaluate_position(board)


def evaluate_mobility(board: chess.Board) -> int:
    original_turn = board.turn
    white_mobility = len(list(board.legal_moves))

    board.turn = not original_turn
    black_mobility = len(list(board.legal_moves))

    board.turn = original_turn

    mobility_score = (white_mobility - black_mobility) * 10
    return mobility_score if board.turn == chess.WHITE else -mobility_score


def evaluate_attacks(board: chess.Board) -> int:
    score = 0
    king_square = board.king(chess.WHITE)
    if king_square:
        attackers = board.attackers(chess.BLACK, king_square)
        score -= len(attackers) * 20

    king_square = board.king(chess.BLACK)
    if king_square:
        attackers = board.attackers(chess.WHITE, king_square)
        score += len(attackers) * 20

    return score


def evaluate_development(board: chess.Board) -> int:
    score = 0
    if board.turn == chess.WHITE:
        b2 = board.piece_at(chess.B2)
        d1 = board.piece_at(chess.D1)
        f1 = board.piece_at(chess.F1)
        g1 = board.piece_at(chess.G1)

        if b2 == chess.Piece(chess.BISHOP, chess.BLACK):
            score -= 20
        if g1 == chess.Piece(chess.KING, chess.BLACK):
            score -= 30
    else:
        b7 = board.piece_at(chess.B7)
        d8 = board.piece_at(chess.D8)
        f8 = board.piece_at(chess.F8)
        g8 = board.piece_at(chess.G8)

        if b7 == chess.Piece(chess.BISHOP, chess.WHITE):
            score += 20
        if g8 == chess.Piece(chess.KING, chess.WHITE):
            score += 30

    return score


def evaluate_center_control(board: chess.Board) -> int:
    center_squares = [chess.E4, chess.D4, chess.E5, chess.D5]
    score = 0

    for square in center_squares:
        piece = board.piece_at(square)
        if piece:
            if piece.color == chess.WHITE:
                score += 10
            else:
                score -= 10

        attackers_white = board.attackers(chess.WHITE, square)
        attackers_black = board.attackers(chess.BLACK, square)

        score += len(attackers_white) * 5
        score -= len(attackers_black) * 5

    return score


def evaluate_pawn_structure(board: chess.Board) -> int:
    score = 0

    for color in [chess.WHITE, chess.BLACK]:
        for square in board.pieces(chess.PAWN, color):
            file = chess.file_of(square)
            rank = chess.rank_of(square)

            doubled = False
            backward = False
            isolated = False

            forward = 1 if color == chess.WHITE else -1
            same_file_pawns = [
                s for s in board.pieces(chess.PAWN, color) if chess.file_of(s) == file
            ]
            if len(same_file_pawns) > 1:
                doubled = True

            if rank + forward < 7 and rank + forward >= 0:
                front_square = chess.square(file, rank + forward)
                if not board.piece_at(front_square):
                    support_square = (
                        chess.square(file - 1, rank + forward) if file > 0 else None
                    )
                    attack_square = (
                        chess.square(file + 1, rank + forward) if file < 7 else None
                    )

                    supported = False
                    attacked = False

                    if support_square and board.piece_at(support_square):
                        front_support = board.piece_at(support_square)
                        if front_support and front_support.piece_type == chess.PAWN:
                            if front_support.color == color:
                                supported = True

                    if attack_square and board.piece_at(attack_square):
                        front_attack = board.piece_at(attack_square)
                        if front_attack and front_attack.piece_type == chess.PAWN:
                            if front_attack.color != color:
                                attacked = True

                    if not supported and not attacked and rank not in [0, 7]:
                        backward = True

            neighbor_files = [f for f in [file - 1, file + 1] if 0 <= f <= 7]
            has_neighbor = any(
                chess.square(f, rank) in board.pieces(chess.PAWN, color)
                for f in neighbor_files
            )
            if not has_neighbor:
                isolated = True

            if doubled:
                score -= 20 if color == chess.WHITE else -20
            if backward:
                score -= 15 if color == chess.WHITE else -15
            if isolated:
                score -= 30 if color == chess.WHITE else -30

    return score


def evaluate_king_safety(board: chess.Board) -> int:
    score = 0

    for color in [chess.WHITE, chess.BLACK]:
        king_square = board.king(color)
        if not king_square:
            continue

        rank = chess.rank_of(king_square)
        file = chess.file_of(king_square)

        pawn_shield = 0
        for f in range(max(0, file - 1), min(8, file + 2)):
            for r in range(max(0, rank - 1), min(8, rank + 2)):
                square = chess.square(f, r)
                piece = board.piece_at(square)
                if piece and piece.piece_type == chess.PAWN and piece.color == color:
                    pawn_shield += 10

        castling_rights = board.castling_rights
        if color == chess.WHITE:
            if chess.WHITE & castling_rights:
                pawn_shield += 20
        else:
            if chess.BLACK & castling_rights:
                pawn_shield += 20

        if color == chess.WHITE:
            score += pawn_shield
        else:
            score -= pawn_shield

    return score


class NNUEevaluator:
    def __init__(self):
        self.feature_indices = [
            (chess.PAWN, 0),
            (chess.PAWN, 1),
            (chess.PAWN, 2),
            (chess.PAWN, 3),
            (chess.KNIGHT, 0),
            (chess.KNIGHT, 1),
            (chess.BISHOP, 0),
            (chess.BISHOP, 1),
            (chess.ROOK, 0),
            (chess.ROOK, 1),
            (chess.QUEEN, 0),
        ]

        layer_sizes = [len(self.feature_indices), 128, 64, 32, 1]
        self.weights = []
        self.biases = []

        np.random.seed(42)
        for i in range(len(layer_sizes) - 1):
            w = np.random.randn(layer_sizes[i], layer_sizes[i + 1]) * 0.1
            b = np.zeros(layer_sizes[i + 1])
            self.weights.append(w)
            self.biases.append(b)

    def extract_features(self, board: chess.Board) -> np.ndarray:
        features = np.zeros(len(self.feature_indices), dtype=np.float32)
        feature_idx = 0

        for piece_type, variant in self.feature_indices:
            for color in [chess.WHITE, chess.BLACK]:
                for square in board.pieces(piece_type, color):
                    rank = chess.rank_of(square)
                    file = chess.file_of(square)

                    if color == chess.BLACK:
                        rank = 7 - rank
                        file = 7 - file

                    idx = (rank * 8 + file + variant * 64) % len(features)
                    features[feature_idx] = 1.0
                    feature_idx += 1

        return features

    def relu(self, x: np.ndarray) -> np.ndarray:
        return np.maximum(0, x)

    def sigmoid(self, x: np.ndarray) -> float:
        return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))

    def forward(self, board: chess.Board) -> int:
        features = self.extract_features(board)

        activation = features
        for i in range(len(self.weights) - 1):
            activation = self.relu(np.dot(activation, self.weights[i]) + self.biases[i])

        output = np.dot(activation, self.weights[-1]) + self.biases[-1]
        score = float(output[0]) * 100

        perspective = 1 if board.turn == chess.WHITE else -1
        return int(score * perspective)

    def evaluate(self, board: chess.Board) -> int:
        if board.is_checkmate():
            return -9999 if board.turn else 9999
        if board.is_stalemate() or board.is_insufficient_material():
            return 0

        return self.forward(board)


def evaluate_combined(board: chess.Board) -> int:
    base_score = evaluate_position(board)
    mobility_score = evaluate_mobility(board)
    attack_score = evaluate_attacks(board)
    center_score = evaluate_center_control(board)
    pawn_score = evaluate_pawn_structure(board)
    king_score = evaluate_king_safety(board)

    total = (
        base_score * 1.0
        + mobility_score * 0.1
        + attack_score * 0.2
        + center_score * 0.1
        + pawn_score * 0.3
        + king_score * 0.2
    )

    return int(total)
