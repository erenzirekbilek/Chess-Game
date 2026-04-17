import chess
import json
import random
from typing import Optional
from pathlib import Path


class OpeningBook:
    def __init__(self, book_file: Optional[str] = None):
        self.book_moves = {}
        if book_file and Path(book_file).exists():
            self.load_book(book_file)
        else:
            self._init_default_book()

    def _init_default_book(self):
        common_opening_moves = {
            "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3": [
                ("e2e4", 0.4),
                ("d2d4", 0.3),
                ("g1f3", 0.2),
                ("b1c3", 0.1),
            ],
            "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 3 2": [
                ("e7e5", 0.35),
                ("c7c5", 0.25),
                ("e7e6", 0.15),
                ("g8f6", 0.15),
                ("d7d6", 0.10),
            ],
            "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1": [
                ("e1g1", 0.30),
                ("d1h5", 0.25),
                ("g1f3", 0.20),
                ("b1c3", 0.15),
                ("f1c4", 0.10),
            ],
            "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1": [
                ("e8g8", 0.30),
                ("b8c6", 0.20),
                ("g8f6", 0.20),
                ("c7c5", 0.15),
                ("e7e5", 0.15),
            ],
            "r1bqkbnr/pppp1ppp/2n5/4p3/B3P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 3": [
                ("e2e4", 0.35),
                ("d2d4", 0.25),
                ("f3e5", 0.20),
                ("a3f8", 0.10),
                ("d1d2", 0.10),
            ],
            "r1bqkbnr/pppp1ppp/2n5/4p3/B3P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 4 3": [
                ("e7e5", 0.40),
                ("c7c5", 0.25),
                ("e7e6", 0.20),
                ("g8f6", 0.15),
            ],
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1": [
                ("e1g1", 0.25),
                ("d1h5", 0.20),
                ("g1f3", 0.20),
                ("b1c3", 0.15),
                ("f1c4", 0.10),
                ("f1b5", 0.05),
                ("d1g4", 0.03),
                ("d1f3", 0.02),
            ],
            "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1": [
                ("e1g1", 0.30),
                ("d1h5", 0.25),
                ("g1f3", 0.20),
                ("b1c3", 0.15),
                ("f1c4", 0.10),
            ],
            "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1": [
                ("e8g8", 0.30),
                ("b8c6", 0.20),
                ("g8f6", 0.20),
                ("c7c5", 0.15),
                ("e7e5", 0.15),
            ],
            "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3": [
                ("e2e4", 0.40),
                ("d2d4", 0.30),
                ("g1f3", 0.20),
                ("b1c3", 0.10),
            ],
            "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 3 2": [
                ("e7e5", 0.35),
                ("c7c5", 0.25),
                ("e7e6", 0.15),
                ("g8f6", 0.15),
                ("d7d6", 0.10),
            ],
            "rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 4 4": [
                ("e2e4", 0.35),
                ("d2d4", 0.30),
                ("g1f3", 0.25),
                ("b1c3", 0.10),
            ],
            "rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 4 4": [
                ("e7e5", 0.35),
                ("c7c5", 0.25),
                ("e7e6", 0.20),
                ("g8f6", 0.20),
            ],
            "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 4 4": [
                ("e2e4", 0.40),
                ("d2d4", 0.30),
                ("b1c3", 0.15),
                ("g1f3", 0.15),
            ],
            "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 4 4": [
                ("e7e5", 0.35),
                ("c7c5", 0.30),
                ("e7e6", 0.20),
                ("g8f6", 0.15),
            ],
            "rnbqkbnr/pppp1ppp/8/2pp4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2": [
                ("e1g1", 0.25),
                ("d1h5", 0.20),
                ("b1c3", 0.20),
                ("g1f3", 0.15),
                ("f1c4", 0.15),
                ("d1f3", 0.05),
            ],
            "rnbqkbnr/pppp1ppp/8/2pp4/4P3/8/PPPP1PPP/RNBQKBNR b KQkq c6 0 2": [
                ("e8g8", 0.25),
                ("b8c6", 0.20),
                ("g8f6", 0.20),
                ("c7c5", 0.20),
                ("e7e5", 0.15),
            ],
            "rnbqkbnr/pppp1ppp/8/4p3/2ppP3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 3": [
                ("e1g1", 0.25),
                ("d1h5", 0.20),
                ("g1f3", 0.20),
                ("b1c3", 0.15),
                ("f1c4", 0.10),
                ("f1d3", 0.10),
            ],
            "rnbqkbnr/pppp1ppp/8/4p3/2ppP3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 3": [
                ("e8g8", 0.25),
                ("a7a6", 0.20),
                ("b8c6", 0.20),
                ("g8f6", 0.15),
                ("c7c5", 0.10),
                ("e7e5", 0.10),
            ],
            "r1bqkbnr/pppp1ppp/2n5/4p3/B3P3/8/PPPP1PPP/RNBQK2R w KQkq - 0 4": [
                ("e2e4", 0.40),
                ("d2d4", 0.30),
                ("f1c4", 0.20),
                ("c1a3", 0.10),
            ],
            "r1bqkbnr/pppp1ppp/2n5/4p3/B3P3/8/PPPP1PPP/RNBQK2R b KQkq - 0 4": [
                ("e7e5", 0.35),
                ("c7c5", 0.25),
                ("e7e6", 0.25),
                ("g8f6", 0.15),
            ],
            "rnbqkb1r/pppp1ppp/5n2/4p3/3P4/8/PPP2PPP/RNBQKBNR w KQkq - 0 4": [
                ("e1g1", 0.25),
                ("d1h5", 0.20),
                ("g1f3", 0.20),
                ("b1c3", 0.15),
                ("f1c4", 0.15),
                ("f1b5", 0.05),
            ],
            "rnbqkb1r/pppp1ppp/5n2/4p3/3P4/8/PPP2PPP/RNBQKBNR b KQkq - 0 4": [
                ("e8g8", 0.30),
                ("b8c6", 0.20),
                ("g8f6", 0.20),
                ("e7e5", 0.15),
                ("c7c5", 0.15),
            ],
            "rnbqkbnr/pppp1ppp/8/8/4p3/4P3/PPPP2PP/RNBQKBNR b KQkq - 0 2": [
                ("e5e4", 0.30),
                ("d5d4", 0.20),
                ("c5c4", 0.15),
                ("b5b4", 0.10),
                ("f5f4", 0.10),
                ("a5a4", 0.05),
                ("g5g4", 0.05),
                ("h5h4", 0.05),
            ],
            "rnbqkbnr/pppp2pp/5p2/8/4p3/4P3/PPPP2PP/RNBQKBNR w KQkq - 0 3": [
                ("e1g1", 0.30),
                ("d1h5", 0.25),
                ("g1f3", 0.25),
                ("b1c3", 0.10),
                ("f1c4", 0.10),
            ],
            "rnbqkbnr/pppp2pp/5p2/8/4p3/4P3/PPPP2PP/RNBQKBNR b KQkq - 0 3": [
                ("e4e3", 0.30),
                ("e4d3", 0.20),
                ("c5c4", 0.15),
                ("d5d4", 0.15),
                ("b5b4", 0.10),
                ("a5a4", 0.10),
            ],
            "rnbqkbnr/pppp2pp/5p2/8/3p4/4P3/PPP2PPP/RNBQKBNR w KQkq - 0 2": [
                ("e1g1", 0.30),
                ("g1f3", 0.25),
                ("d1h5", 0.20),
                ("b1c3", 0.15),
                ("f1c4", 0.10),
            ],
            "rnbqkbnr/pppp2pp/5p2/8/3p4/4P3/PPP2PPP/RNBQKBNR b KQkq - 0 2": [
                ("e8g8", 0.25),
                ("b8c6", 0.20),
                ("g8f6", 0.20),
                ("d4d3", 0.20),
                ("c5c4", 0.15),
            ],
            "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQ1K2R w KQkq - 4 4": [
                ("e2e4", 0.35),
                ("d2d4", 0.30),
                ("f3e5", 0.15),
                ("c1a3", 0.10),
                ("d1d2", 0.10),
            ],
            "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQ1K2R b KQkq - 4 4": [
                ("e7e5", 0.35),
                ("c7c5", 0.30),
                ("e7e6", 0.20),
                ("g8f6", 0.15),
            ],
            "rnbqkb1r/p3nppp/p7/1pp4/2p1P3/2N5/PPP2PPP/R1BQKBNR w KQkq b6 0 5": [
                ("e1g1", 0.30),
                ("d1h5", 0.25),
                ("g1f3", 0.20),
                ("b1c3", 0.15),
                ("f1c4", 0.10),
            ],
            "rnbqkb1r/p3nppp/p7/1pp4/2p1P3/2N5/PPP2PPP/R1BQKBNR b KQkq b6 0 5": [
                ("e8g8", 0.25),
                ("a7a6", 0.20),
                ("b8c6", 0.20),
                ("g8f6", 0.15),
                ("c7c5", 0.10),
                ("e7e5", 0.10),
            ],
            "r1bqk2r/pppp1ppp/2n5/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 5 4": [
                ("e2e4", 0.40),
                ("d2d4", 0.30),
                ("f3e5", 0.15),
                ("c1a3", 0.10),
                ("d1d2", 0.05),
            ],
            "r1bqk2r/pppp1ppp/2n5/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 5 4": [
                ("e7e5", 0.35),
                ("c7c5", 0.30),
                ("e7e6", 0.20),
                ("g8f6", 0.15),
            ],
            "rnbqkb1r/pppp1ppp/5n2/4p2Q/4P3/2N5/PPP2PPP/R1B1KBNR w KQkq - 5 4": [
                ("e2e4", 0.35),
                ("d2d4", 0.30),
                ("e4e5", 0.15),
                ("h5f7", 0.10),
                ("h5g5", 0.10),
            ],
            "rnbqkb1r/pppp1ppp/5n2/4p2Q/4P3/2N5/PPP2PPP/R1B1KBNR b KQkq - 5 4": [
                ("e7e5", 0.35),
                ("c7c5", 0.30),
                ("e7e6", 0.20),
                ("g8f6", 0.15),
            ],
            "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 4": [
                ("e2e4", 0.40),
                ("d2d4", 0.30),
                ("f3e5", 0.15),
                ("c1a3", 0.10),
                ("d1d2", 0.05),
            ],
            "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 0 4": [
                ("e7e5", 0.35),
                ("c7c5", 0.30),
                ("e7e6", 0.20),
                ("g8f6", 0.15),
            ],
        }

        for fen, moves in common_opening_moves.items():
            self.book_moves[fen] = moves

    def load_book(self, book_file: str):
        with open(book_file, "r") as f:
            data = json.load(f)
            for entry in data:
                fen = entry["fen"]
                moves = [
                    (m["uci"], m.get("weight", 1.0)) for m in entry.get("moves", [])
                ]
                self.book_moves[fen] = moves

    def save_book(self, book_file: str):
        data = []
        for fen, moves in self.book_moves.items():
            entry = {
                "fen": fen,
                "moves": [{"uci": m[0], "weight": m[1]} for m in moves],
            }
            data.append(entry)

        with open(book_file, "w") as f:
            json.dump(data, f, indent=2)

    def get(self, board: chess.Board) -> Optional[chess.Move]:
        fen = board.fen()
        if fen in self.book_moves:
            moves_weights = self.book_moves[fen]
            total = sum(w for _, w in moves_weights)
            r = random.random() * total

            cumulative = 0
            for uci, weight in moves_weights:
                cumulative += weight
                if cumulative >= r:
                    return chess.Move.from_uci(uci)

        return None

    def add(self, board: chess.Board, move: chess.Move, weight: float = 1.0):
        fen = board.fen()
        uci = move.uci()

        if fen not in self.book_moves:
            self.book_moves[fen] = []

        for i, (existing_uci, existing_weight) in enumerate(self.book_moves[fen]):
            if existing_uci == uci:
                self.book_moves[fen][i] = (uci, existing_weight + weight)
                return

        self.book_moves[fen].append((uci, weight))

    def has_moves(self, board: chess.Board) -> bool:
        fen = board.fen()
        return fen in self.book_moves and len(self.book_moves[fen]) > 0
