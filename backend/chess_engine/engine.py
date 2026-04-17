import chess
from typing import Optional
from enum import Enum

from .minimax import minimax, evaluate_position
from .alphabeta import alpha_beta_search, iterative_deepening, aspiration_window
from .mcts import mcts_search
from .quiescence import search_with_quiescence
from .evaluation import evaluate_combined, NNUEevaluator
from .opening_book import OpeningBook
from .tablebases import Tablebase


class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3
    EXPERT = 4


DEPTH_MAPPING = {
    Difficulty.EASY: 2,
    Difficulty.MEDIUM: 3,
    Difficulty.HARD: 4,
    Difficulty.EXPERT: 6,
}


class ChessEngine:
    def __init__(
        self,
        difficulty: Difficulty = Difficulty.MEDIUM,
        use_opening_book: bool = True,
        use_tablebase: bool = True,
        use_nnue: bool = False,
        max_time: float = 2.0,
    ):
        self.difficulty = difficulty
        self.depth = DEPTH_MAPPING[difficulty]
        self.use_opening_book = use_opening_book
        self.use_tablebase = use_tablebase
        self.use_nnue = use_nnue
        self.max_time = max_time

        self.opening_book = OpeningBook() if use_opening_book else None
        self.tablebase = Tablebase() if use_tablebase else None
        self.nnue = NNUEevaluator() if use_nnue else None

        self.nodes_searched = 0
        self.eval_calls = 0

    def set_difficulty(self, difficulty: Difficulty):
        self.difficulty = difficulty
        self.depth = DEPTH_MAPPING[difficulty]

    def evaluate(self, board: chess.Board) -> int:
        self.eval_calls += 1
        if self.use_nnue and self.nnue:
            return self.nnue.evaluate(board)
        return evaluate_combined(board)

    def get_opening_move(self, board: chess.Board) -> Optional[chess.Move]:
        if self.opening_book and self.opening_book.has_moves(board):
            return self.opening_book.get(board)
        return None

    def get_tablebase_move(self, board: chess.Board) -> Optional[chess.Move]:
        if self.tablebase and self.tablebase.has_tablebase(board):
            return self.tablebase.get_best_move(board)
        return None

    def search_minimax(self, board: chess.Board) -> tuple[Optional[chess.Move], int]:
        self.nodes_searched = 0
        return minimax(board, self.depth, board.turn == chess.WHITE)

    def search_alphabeta(self, board: chess.Board) -> tuple[Optional[chess.Move], int]:
        self.nodes_searched = 0
        return alpha_beta_search(
            board, self.depth, maximizing=board.turn == chess.WHITE
        )

    def search_iterative(self, board: chess.Board) -> tuple[Optional[chess.Move], int]:
        self.nodes_searched = 0
        return iterative_deepening(board, max_depth=self.depth)

    def search_mcts(self, board: chess.Board) -> tuple[Optional[chess.Move], int]:
        iterations = {
            Difficulty.EASY: 100,
            Difficulty.MEDIUM: 300,
            Difficulty.HARD: 500,
            Difficulty.EXPERT: 800,
        }
        iters = iterations[self.difficulty]
        move = mcts_search(board, iterations=iters)
        score = self.evaluate(board)
        return move, score

    def search_quiescence(self, board: chess.Board) -> tuple[Optional[chess.Move], int]:
        self.nodes_searched = 0
        depth = max(1, self.depth - 1)
        score = search_with_quiescence(
            board, depth, alpha=float("-inf"), beta=float("inf")
        )
        best_move = None
        for move in board.legal_moves:
            new_board = board.copy()
            new_board.push(move)
            move_score = self.evaluate(new_board)
            if best_move is None or move_score > score:
                score = move_score
                best_move = move
        return best_move, score

    def search_hybrid(self, board: chess.Board) -> tuple[Optional[chess.Move], int]:
        if self.opening_book and self.opening_book.has_moves(board):
            opening_move = self.opening_book.get(board)
            if opening_move:
                score = self.evaluate(board)
                return opening_move, score

        if self.tablebase and self.tablebase.has_tablebase(board):
            tb_move = self.tablebase.get_best_move(board)
            if tb_move:
                score = self.evaluate(board)
                return tb_move, score

        if self.difficulty == Difficulty.EASY:
            return self.search_minimax(board)
        elif self.difficulty == Difficulty.MEDIUM:
            return self.search_alphabeta(board)
        elif self.difficulty == Difficulty.HARD:
            return self.search_quiescence(board)
        else:
            return self.search_iterative(board)

    def get_best_move(
        self,
        board: chess.Board,
        method: str = "hybrid",
    ) -> Optional[chess.Move]:
        if board.is_game_over():
            return None

        if method == "minimax":
            move, _ = self.search_minimax(board)
        elif method == "alphabeta":
            move, _ = self.search_alphabeta(board)
        elif method == "iterative":
            move, _ = self.search_iterative(board)
        elif method == "mcts":
            move, _ = self.search_mcts(board)
        elif method == "quiescence":
            move, _ = self.search_quiescence(board)
        elif method == "hybrid":
            move, _ = self.search_hybrid(board)
        else:
            move, _ = self.search_alphabeta(board)

        return move

    def get_move_with_score(
        self,
        board: chess.Board,
        method: str = "hybrid",
    ) -> tuple[Optional[chess.Move], int]:
        if method == "minimax":
            return self.search_minimax(board)
        elif method == "alphabeta":
            return self.search_alphabeta(board)
        elif method == "iterative":
            return self.search_iterative(board)
        elif method == "mcts":
            return self.search_mcts(board)
        elif method == "quiescence":
            return self.search_quiescence(board)
        else:
            return self.search_hybrid(board)

    def play_move(self, board: chess.Board, method: str = "hybrid") -> bool:
        move = self.get_best_move(board, method)
        if move:
            board.push(move)
            if self.opening_book:
                self.opening_book.add(board, move)
            return True
        return False

    def get_stats(self) -> dict:
        return {
            "difficulty": self.difficulty.name,
            "depth": self.depth,
            "nodes_searched": self.nodes_searched,
            "eval_calls": self.eval_calls,
        }

    def reset_stats(self):
        self.nodes_searched = 0
        self.eval_calls = 0


def create_engine(
    difficulty: str = "medium",
    use_book: bool = True,
    use_tablebase: bool = True,
    use_nnue: bool = False,
) -> ChessEngine:
    diff_map = {
        "easy": Difficulty.EASY,
        "medium": Difficulty.MEDIUM,
        "hard": Difficulty.HARD,
        "expert": Difficulty.EXPERT,
    }
    difficulty_enum = diff_map.get(difficulty.lower(), Difficulty.MEDIUM)

    return ChessEngine(
        difficulty=difficulty_enum,
        use_opening_book=use_book,
        use_tablebase=use_tablebase,
        use_nnue=use_nnue,
    )
