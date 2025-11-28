"""
Performance Optimization Configuration for Chinese Chess AI
This module contains optimization settings and best practices
"""

# Cache Settings
CACHE_SIZE = 65536  # Maximum cache entries for board hashes and states
PIECE_CACHE_SIZE = 10000  # Cache for piece move calculations

# Minimax Optimization
TRANSPOSITION_TABLE_SIZE = 100000  # Store computed positions
KILLER_MOVE_CUTOFF_DEPTH = 4  # Use killer move heuristic at this depth
ITERATIVE_DEEPENING_THRESHOLD = 6  # Enable iterative deepening

# MCTS Optimization
MCTS_BATCH_SIZE = 4  # Number of simulations to batch together
MCTS_CACHE_MOVES = True  # Cache frequently visited moves
MCTS_EARLY_TERMINATION = 0.95  # Stop if confidence reaches this threshold

# Memory Management
GARBAGE_COLLECTION_INTERVAL = 100  # Run GC every N iterations
MAX_TREE_NODES = 50000  # Maximum nodes to keep in memory

# Performance Monitoring
ENABLE_PROFILING = False  # Set True to enable performance profiling
PROFILE_OUTPUT_FILE = "profile_results.txt"

# Evaluation Optimization
PIECE_SQUARE_TABLE = {
    'RG': {  # Red General
        (3, 3): 0, (3, 4): 10, (3, 5): 0,
        (4, 3): 10, (4, 4): 20, (4, 5): 10,
        (5, 3): 0, (5, 4): 10, (5, 5): 0,
    },
    'BG': {  # Black General
        (3, 3): 0, (3, 4): 10, (3, 5): 0,
        (4, 3): 10, (4, 4): 20, (4, 5): 10,
        (5, 3): 0, (5, 4): 10, (5, 5): 0,
    }
}

# AI Strategy
USE_OPENING_BOOK = False  # Use predefined opening moves
USE_ENDGAME_TABLES = False  # Use precomputed endgame solutions
DYNAMIC_DEPTH_ADJUSTMENT = True  # Adjust search depth based on position complexity

# Parallel Processing
USE_MULTITHREADING = False  # Enable multithreading (experimental)
NUM_THREADS = 4  # Number of threads for parallel search
