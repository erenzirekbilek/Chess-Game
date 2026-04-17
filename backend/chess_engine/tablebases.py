import chess
import json
from typing import Optional, Dict, Tuple
from pathlib import Path


class Tablebase:
    def __init__(self, tablebase_dir: Optional[str] = None):
        self.tablebase: Dict[str, dict] = {}
        if tablebase_dir:
            self.load_tablebase(tablebase_dir)
        else:
            self._init_minimal_tablebase()

    def _init_minimal_tablebase(self):
        known_endgames = {
            "KQK": {chess.WHITE: 1.0, chess.BLACK: -1.0, "moves": 10},
            "KRK": {chess.WHITE: 1.0, chess.BLACK: -1.0, "moves": 6},
            "KBK": {chess.WHITE: 0.5, chess.BLACK: -0.5, "moves": 0},
            "KNNK": {chess.WHITE: 0.5, chess.BLACK: -0.5, "moves": 0},
            "KPK": {chess.WHITE: 0.5, chess.BLACK: -0.5, "moves": 0},
            "KBNK": {chess.WHITE: 1.0, chess.BLACK: -1.0, "moves": 0},
            "KRPKR": {chess.WHITE: 0.0, chess.BLACK: 0.0, "moves": 0},
        }

        for endgame, result in known_endgames.items():
            self.tablebase[endgame] = result

    def load_tablebase(self, tablebase_dir: str):
        path = Path(tablebase_dir)
        if not path.exists():
            return

        for file in path.glob("*.json"):
            with open(file, "r") as f:
                data = json.load(f)
                for entry in data:
                    key = entry["key"]
                    self.tablebase[key] = entry

    def save_tablebase(self, tablebase_dir: str):
        path = Path(tablebase_dir)
        path.mkdir(parents=True, exist_ok=True)

        for key, entry in self.tablebase.items():
            filename = key.replace(" ", "_").replace("/", "_") + ".json"
            filepath = path / filename

            with open(filepath, "w") as f:
                json.dump(entry, f, indent=2)

    def _key_from_board(self, board: chess.Board) -> str:
        pieces = []

        white_pieces = []
        black_pieces = []

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.piece_type != chess.KING:
                symbol = piece.symbol().upper()
                if piece.color == chess.WHITE:
                    white_pieces.append(symbol)
                else:
                    black_pieces.append(symbol)

        white_pieces.sort()
        black_pieces.sort()

        key = "K" + "".join(white_pieces) + "K" + "".join(black_pieces)
        return key

    def _key_from_pieces(
        self,
        white_king: chess.Square,
        white_pieces: list,
        black_king: chess.Square,
        black_pieces: list,
    ) -> str:
        white_symbols = ["K"]
        black_symbols = ["K"]

        for piece_type in white_pieces:
            symbol = chess.PIECE_SYMBOLS[piece_type].upper()
            white_symbols.append(symbol)

        for piece_type in black_pieces:
            symbol = chess.PIECE_SYMBOLS[piece_type].upper()
            black_symbols.append(symbol)

        white_symbols.sort()
        black_symbols.sort()

        return "".join(white_symbols) + "".join(black_symbols)

    def probe(self, board: chess.Board) -> Optional[dict]:
        if not board.is_game_over():
            return None

        key = self._key_from_board(board)

        if key in self.tablebase:
            return self.tablebase[key]

        return None

    def probe_wdl(self, board: chess.Board) -> Optional[int]:
        result = self.probe(board)
        if result:
            return result.get("wdl", 0)
        return None

    def probe_dtz(self, board: chess.Board) -> Optional[int]:
        result = self.probe(board)
        if result:
            return result.get("dtz", 0)
        return None

    def get_result(self, board: chess.Board) -> Optional[str]:
        if not board.is_game_over():
            return None

        if board.is_checkmate():
            winner = board.turn
            return "1-0" if not winner else "0-1"

        if board.is_stalemate():
            return "1/2-1/2"

        if board.is_insufficient_material():
            return "1/2-1/2"

        result = self.probe_wdl(board)
        if result is not None:
            if result > 0:
                return "1-0"
            elif result < 0:
                return "0-1"
            else:
                return "1/2-1/2"

        return None

    def has_tablebase(self, board: chess.Board) -> bool:
        key = self._key_from_board(board)
        return key in self.tablebase

    def get_best_move(self, board: chess.Board) -> Optional[chess.Move]:
        if board.is_game_over():
            return None

        key = self._key_from_board(board)

        if key not in self.tablebase:
            return None

        tb = self.tablebase[key]
        best_wdl = -2
        best_move = None
        best_dtz = 1000

        for move in board.legal_moves:
            new_board = board.copy()
            new_board.push(move)

            if new_board.is_game_over():
                outcome = new_board.outcome()
                if outcome.winner == chess.WHITE:
                    wdl = 1
                elif outcome.winner == chess.BLACK:
                    wdl = -1
                else:
                    wdl = 0

                if wdl > best_wdl:
                    best_wdl = wdl
                    best_move = move
                    best_dtz = 0
            else:
                result = self.probe_wdl(new_board)
                if result is not None:
                    if result > best_wdl:
                        best_wdl = result
                        best_move = move
                        dtz = self.probe_dtz(new_board)
                        best_dtz = dtz if dtz else 1000

        return best_move

    def is_mate(self, board: chess.Board) -> bool:
        result = self.probe_wdl(board)
        if result is not None:
            return abs(result) == 1
        return False

    def is_drawn(self, board: chess.Board) -> bool:
        result = self.probe_wdl(board)
        if result is not None:
            return result == 0
        return False

    def winning_side(self, board: chess.Board) -> Optional[chess.Color]:
        result = self.probe_wdl(board)
        if result is not None:
            if result > 0:
                return chess.WHITE
            elif result < 0:
                return chess.BLACK
        return None

    def distance_to_zero(self, board: chess.Board) -> Optional[int]:
        if board.turn == chess.WHITE:
            return self.probe_dtz(board)
        else:
            dtz = self.probe_dtz(board)
            if dtz is not None and dtz > 0:
                return -dtz
            return dtz


def simplify_to_key(
    white_pieces: list,
    black_pieces: list,
) -> str:
    white_sorted = sorted([p.symbol().upper() for p in white_pieces])
    black_sorted = sorted([p.symbol().upper() for p in black_pieces])

    white_key = "K" + "".join(white_sorted)
    black_key = "K" + "".join(black_sorted)

    return white_key + black_key


def classify_position(board: chess.Board) -> str:
    white_pieces = []
    black_pieces = []

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and piece.piece_type != chess.KING:
            symbol = piece.symbol().upper()
            if piece.color == chess.WHITE:
                white_pieces.append(symbol)
            else:
                black_pieces.append(symbol)

    return simplify_to_key(white_pieces, black_pieces)


class SyzygyTablebase(Tablebase):
    def __init__(self, tablebase_dir: Optional[str] = None, max_pieces: int = 7):
        super().__init__(tablebase_dir)
        self.max_pieces = max_pieces

    def can_probe(self, board: chess.Board) -> bool:
        num_pieces = len(board.piece_map())

        if num_pieces > self.max_pieces + 2:
            return False

        key = self._key_from_board(board)
        return key in self.tablebase

    def probe_root(
        self, board: chess.Board, as_white: bool = True
    ) -> Optional[Tuple[chess.Move, int, int, int]]:
        if not self.can_probe(board):
            return None

        best_move = None
        best_wdl = -2
        best_dtz = 1000
        best_result = None

        for move in board.legal_moves:
            new_board = board.copy()
            new_board.push(move)

            wdl = self.probe_wdl(new_board)
            dtz = self.probe_dtz(new_board)

            if wdl is not None:
                if as_white:
                    effective_wdl = wdl if board.turn == chess.WHITE else -wdl
                else:
                    effective_wdl = wdl if board.turn == chess.BLACK else -wdl

                if effective_wdl > best_wdl:
                    best_wdl = effective_wdl
                    best_move = move
                    best_dtz = dtz if dtz else 1000
                    best_result = wdl

        if best_move:
            return (best_move, best_wdl, best_dtz, best_result)

        return None


def distance_to_mate(board: chess.Board) -> int:
    if not board.is_checkmate():
        return 0

    return 1


def find_tablebase_moves(board: chess.Board) -> list[chess.Move]:
    moves = []

    if not board.is_game_over():
        tb = Tablebase()
        best_move = tb.get_best_move(board)
        if best_move:
            moves.append(best_move)

    return moves
