import chess
import math
import random
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class MCTSNode:
    board: chess.Board
    parent: Optional["MCTSNode"] = None
    move: Optional[chess.Move] = None
    children: list["MCTSNode"] = field(default_factory=list)
    visits: int = 0
    wins: int = 0
    untried_moves: list[chess.Move] = field(default_factory=list)

    def __post_init__(self):
        if not self.untried_moves and self.board:
            self.untried_moves = list(self.board.legal_moves)


class MCTS:
    def __init__(self, board: chess.Board, exploration_constant: float = 1.41):
        self.root = MCTSNode(board)
        self.exploration_constant = exploration_constant

    def uct_select(self, node: MCTSNode) -> MCTSNode:
        if not node.children:
            return node

        best_child = None
        best_value = float("-inf")

        for child in node.children:
            if child.visits == 0:
                uct_value = float("inf")
            else:
                uct_value = (
                    child.wins / child.visits
                ) + self.exploration_constant * math.sqrt(
                    math.log(node.visits) / child.visits
                )

            if uct_value > best_value:
                best_value = uct_value
                best_child = child

        return best_child or node

    def expand(self, node: MCTSNode) -> MCTSNode:
        if not node.untried_moves:
            return node

        move = node.untried_moves.pop()
        new_board = node.board.copy()
        new_board.push(move)
        child = MCTSNode(new_board, parent=node, move=move)
        node.children.append(child)
        return child

    def backpropagate(self, node: MCTSNode, result: float):
        while node:
            node.visits += 1
            node.wins += result
            node = node.parent

    def rollout(self, board: chess.Board, max_depth: int = 10) -> float:
        current = board.copy()
        depth = 0

        while not current.is_game_over() and depth < max_depth:
            moves = list(current.legal_moves)
            if not moves:
                break

            move = random.choice(moves)
            current.push(move)
            depth += 1

        if current.is_checkmate():
            return 1.0 if not current.turn else 0.0
        elif current.is_stalemate() or current.is_insufficient_material():
            return 0.5

        return 0.5

    def select_best(self) -> chess.Move:
        if not self.root.children:
            if self.root.board.legal_moves:
                return random.choice(list(self.root.board.legal_moves))
            return None

        best_child = max(self.root.children, key=lambda c: c.visits)
        return best_child.move

    def search(self, iterations: int = 1000) -> chess.Move:
        for _ in range(iterations):
            node = self.root

            while node.children and not node.untried_moves:
                node = self.uct_select(node)

            if node.untried_moves:
                node = self.expand(node)

            result = self.rollout(node.board)
            self.backpropagate(node, result)

        return self.select_best()


def mcts_search(board: chess.Board, iterations: int = 1000) -> chess.Move:
    mcts = MCTS(board)
    return mcts.search(iterations)
