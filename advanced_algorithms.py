"""
Advanced Game Tree Algorithms for Chinese Chess AI
Contains AlphaBeta++, Negamax, and MTD(f) algorithms
"""

from math import inf
from time import time
from abc import abstractmethod
from game_state import GameState
from node import NodeMinimax, NodeMCTS
from team import Team

# Import GameTree base class
from game_tree import GameTree

# Import performance utilities safely
try:
    from performance_utils import transposition_table, performance_monitor
except ImportError:
    # Fallback if performance_utils not available
    transposition_table = None
    performance_monitor = None


class NodeAlphaBeta(NodeMinimax):
    """Node for AlphaBeta++ algorithm with enhanced move ordering"""

    def __init__(self, game_state: GameState, parent, parent_move: tuple) -> None:
        super().__init__(game_state, parent, parent_move)
        self.killer_moves = []  # Killer move heuristic
        self.history = {}  # Move history heuristic

    def get_move_order_score(self, move):
        """Calculate score for move ordering heuristic"""
        score = 0

        # Killer move heuristic
        if move in self.killer_moves:
            score += 1000

        # Capture heuristic (prioritize captures)
        old_pos, new_pos = move
        if self.game_state.board[new_pos[0]][new_pos[1]] != "NN":
            score += 500

        # History heuristic
        score += self.history.get(move, 0)

        return score

    def sort_children_with_heuristic(self):
        """Sort children using move ordering heuristics"""
        if self._is_children_sorted:
            return

        # Calculate scores for each child
        scores = []
        for child in self.list_of_children:
            move = child.parent_move
            score = self.get_move_order_score(move)
            scores.append((score, child))

        # Sort by score (descending)
        scores.sort(key=lambda x: x[0], reverse=True)
        self.list_of_children = [child for _, child in scores]
        self._is_children_sorted = True

    def update_killer_moves(self, move, depth):
        """Update killer move list for this depth"""
        if len(self.killer_moves) < 2:
            self.killer_moves.append(move)
        else:
            self.killer_moves[0] = self.killer_moves[1]
            self.killer_moves[1] = move

    def update_history(self, move, depth):
        """Update history heuristic"""
        self.history[move] = self.history.get(move, 0) + depth * depth

    def _create_node(self, game_state: GameState, parent, parent_move: tuple):
        """Create a new AlphaBeta++ node"""
        return NodeAlphaBeta(game_state, parent, parent_move)


class NodeNegamax(NodeMinimax):
    """Node for Negamax algorithm with transposition table"""

    def __init__(self, game_state: GameState, parent, parent_move: tuple) -> None:
        super().__init__(game_state, parent, parent_move)
        self.hash_value = None

    def negamax(self, depth: int, alpha: float = -inf, beta: float = inf) -> float:
        """Negamax with alpha-beta pruning and transposition table"""

        # Check transposition table
        board_hash = hash(tuple(map(tuple, self.game_state.board)))
        lookup_value = None
        lookup_flag = None
        
        if transposition_table is not None:
            lookup_value, lookup_flag = transposition_table.lookup(board_hash, depth)

            if lookup_value is not None:
                if lookup_flag == 'EXACT':
                    return lookup_value
                elif lookup_flag == 'LOWER':
                    alpha = max(alpha, lookup_value)
                elif lookup_flag == 'UPPER':
                    beta = min(beta, lookup_value)

                if alpha >= beta:
                    return lookup_value

        # Terminal node
        if depth == 0:
            value = self.game_state.value
            if self.game_state._current_team is Team.RED:
                value = -value
            if transposition_table is not None:
                transposition_table.store(board_hash, depth, value, 'EXACT')
            return value

        self.generate_all_children()

        # No moves available
        if len(self.list_of_children) == 0:
            value = -inf if self.game_state._current_team is Team.RED else inf
            if transposition_table is not None:
                transposition_table.store(board_hash, depth, value, 'EXACT')
            return value

        max_value = -inf
        flag = 'UPPER'

        for child in self.list_of_children:
            value = -child.negamax(depth - 1, -beta, -alpha)
            max_value = max(max_value, value)
            alpha = max(alpha, value)

            if alpha >= beta:
                flag = 'LOWER'
                break

        if max_value <= alpha:
            flag = 'UPPER'
        elif max_value >= beta:
            flag = 'LOWER'
        else:
            flag = 'EXACT'

        if transposition_table is not None:
            transposition_table.store(board_hash, depth, max_value, flag)
        return max_value

    def _create_node(self, game_state: GameState, parent, parent_move: tuple):
        """Create a new Negamax node"""
        return NodeNegamax(game_state, parent, parent_move)

    def best_move(self):
        """Return best move for Negamax"""
        best_value = -inf
        best_children = []

        for child in self.list_of_children:
            if child.minimax_value == self.minimax_value:
                best_children.append(child)

        from random import choice
        return choice(best_children) if best_children else self.list_of_children[0]


# ========== GAME TREE IMPLEMENTATIONS ==========

class GameTreeAlphaBeta(GameTree):
    """GameTree using AlphaBeta++ with move ordering heuristics"""

    def __init__(self, team, target_depth, value_pack: int = 0):
        super().__init__(team, value_pack)
        self.target_depth = target_depth

    def _create_node(self, game_state, parent, parent_move) -> NodeAlphaBeta:
        return NodeAlphaBeta(game_state, parent, parent_move)

    def alphabeta_search(self, depth, alpha=-inf, beta=inf) -> float:
        """Perform AlphaBeta search with enhanced move ordering"""
        # Only sort if node has the method
        if hasattr(self.current_node, 'sort_children_with_heuristic'):
            self.current_node.sort_children_with_heuristic()
        return self.current_node.minimax(depth, self.team is Team.RED, alpha, beta)

    def process(self, moves_queue) -> tuple:
        """Execute AlphaBeta++ algorithm"""
        start = time()

        # Perform search
        self.alphabeta_search(self.target_depth)

        # Get best move
        old_pos, new_pos = self.move_to_best_child()
        moves_queue.append((old_pos, new_pos))

        end = time()
        print(f"AlphaBeta++ Value: {self.current_node.minimax_value}")
        print(f"Time: {end - start:.2f}s")
        print(f"{self.team.name} moves: {old_pos} -> {new_pos}")

        return old_pos, new_pos


class GameTreeNegamax(GameTree):
    """GameTree using Negamax with transposition table"""

    def __init__(self, team, target_depth, value_pack: int = 0):
        super().__init__(team, value_pack)
        self.target_depth = target_depth

    def _create_node(self, game_state, parent, parent_move) -> NodeNegamax:
        return NodeNegamax(game_state, parent, parent_move)

    def process(self, moves_queue) -> tuple:
        """Execute Negamax algorithm"""
        start = time()

        # Perform Negamax search
        value = self.current_node.negamax(self.target_depth)

        # Get best move
        old_pos, new_pos = self.move_to_best_child()
        moves_queue.append((old_pos, new_pos))

        end = time()
        print(f"Negamax Value: {value}")
        print(f"Time: {end - start:.2f}s")
        print(f"{self.team.name} moves: {old_pos} -> {new_pos}")

        return old_pos, new_pos


class GameTreeMTD(GameTree):
    """GameTree using MTD(f) - Memory-enhanced Test Driver with Transposition Table"""

    def __init__(self, team, target_depth, value_pack: int = 0):
        super().__init__(team, value_pack)
        self.target_depth = target_depth

    def _create_node(self, game_state, parent, parent_move) -> NodeNegamax:
        return NodeNegamax(game_state, parent, parent_move)

    def negamax_with_bounds(self, depth, bound, alpha=-inf, beta=inf):
        """Negamax with specific bound"""
        if beta <= alpha:
            beta = alpha + 1

        board_hash = hash(tuple(map(tuple, self.current_node.game_state.board)))
        result = self.current_node.negamax(depth, alpha, beta)

        if result < bound:
            return result
        else:
            return result

    def mtdf(self, depth, first_guess=0):
        """MTD(f) algorithm - converges to exact value with multiple searches"""
        upper_bound = inf
        lower_bound = -inf
        guess = first_guess
        iterations = 0

        start_time = time()
        while lower_bound < upper_bound and iterations < 3:  # Limit iterations
            beta = guess if guess == lower_bound else guess + 1

            g = self.negamax_with_bounds(depth, beta, lower_bound, upper_bound)

            if g < beta:
                upper_bound = g
            else:
                lower_bound = g

            guess = g
            iterations += 1

        return guess

    def process(self, moves_queue) -> tuple:
        """Execute MTD(f) algorithm"""
        start = time()

        # Perform MTD(f) search
        value = self.mtdf(self.target_depth)

        # Get best move
        old_pos, new_pos = self.move_to_best_child()
        moves_queue.append((old_pos, new_pos))

        end = time()
        print(f"MTD(f) Value: {value}")
        print(f"Time: {end - start:.2f}s")
        print(f"{self.team.name} moves: {old_pos} -> {new_pos}")

        return old_pos, new_pos


class GameTreeHybrid(GameTree):
    """Hybrid algorithm that switches between Minimax and MCTS based on position"""

    def __init__(self, team, depth_for_minimax=4, time_for_mcts=2, value_pack: int = 0):
        super().__init__(team, value_pack)
        self.depth_for_minimax = depth_for_minimax
        self.time_for_mcts = time_for_mcts
        
        # Import here to avoid circular imports
        from game_tree import GameTreeMCTS
        self.minimax_engine = GameTreeAlphaBeta(team, depth_for_minimax, value_pack)
        self.mcts_engine = GameTreeMCTS(team, time_for_mcts, value_pack) if GameTreeMCTS else None

    def _create_node(self, game_state, parent, parent_move):
        return NodeMinimax(game_state, parent, parent_move)

    def should_use_minimax(self):
        """Determine if position is suitable for minimax"""
        # Use minimax in opening and midgame (high complexity)
        # Use MCTS in endgame (low complexity, high uncertainty)
        child_count = len(self.current_node.game_state.all_child_gamestates)
        piece_count = (
            self.current_node.game_state.number_of_red_pieces +
            self.current_node.game_state.number_of_black_pieces
        )

        # Favor minimax when few pieces remain or many moves available
        return piece_count > 10 or child_count > 20

    def process(self, moves_queue) -> tuple:
        """Execute hybrid algorithm"""
        start = time()

        if self.should_use_minimax():
            print("Using AlphaBeta++ for this position...")
            self.minimax_engine.current_node = self.current_node
            old_pos, new_pos = self.minimax_engine.process(moves_queue)
        elif self.mcts_engine:
            print("Using MCTS for this position...")
            self.mcts_engine.current_node = self.current_node
            old_pos, new_pos = self.mcts_engine.process(moves_queue)
        else:
            # Fallback to minimax if MCTS not available
            print("Fallback to AlphaBeta++")
            self.minimax_engine.current_node = self.current_node
            old_pos, new_pos = self.minimax_engine.process(moves_queue)

        end = time()
        print(f"Hybrid Algorithm Time: {end - start:.2f}s")

        return old_pos, new_pos
