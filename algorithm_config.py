"""
Algorithm Configuration and Best Practices
Cấu hình tối ưu cho mỗi thuật toán
"""

# ========== ALGORITHM CONFIGURATIONS ==========

ALGORITHM_CONFIGS = {
    "Minimax": {
        "display_name": "Minimax (Basic)",
        "description": "Classic minimax with alpha-beta pruning",
        "recommended_depth": 4,
        "memory_usage": "Low",
        "speed": "2/5",
        "quality": "3/5",
        "best_for": "Learning, simple positions",
        "min_depth": 2,
        "max_depth": 5,
    },
    "MCTS": {
        "display_name": "MCTS (Monte Carlo Tree Search)",
        "description": "Probabilistic tree search with simulations",
        "recommended_time": 3,
        "memory_usage": "Medium",
        "speed": "3/5",
        "quality": "3/5",
        "best_for": "Complex positions, exploration",
        "min_time": 1,
        "max_time": 10,
    },
    "DyMinimax": {
        "display_name": "Dynamic Minimax",
        "description": "Adapts depth based on position complexity",
        "recommended_depth": 4,
        "memory_usage": "Low",
        "speed": "2/5",
        "quality": "4/5",
        "best_for": "Balanced play",
        "min_depth": 3,
        "max_depth": 6,
    },
    "DeMinimax": {
        "display_name": "Deepening Minimax",
        "description": "Iterative deepening with depth progression",
        "recommended_depth": 5,
        "memory_usage": "Medium",
        "speed": "2/5",
        "quality": "4/5",
        "best_for": "Time-bounded search",
        "min_depth": 3,
        "max_depth": 7,
    },
    "ExMinimax": {
        "display_name": "Excavation Minimax",
        "description": "Combines minimax with MCTS simulations",
        "recommended_depth": 3,
        "memory_usage": "Medium",
        "speed": "2/5",
        "quality": "4/5",
        "best_for": "Endgame, precise evaluation",
        "min_depth": 2,
        "max_depth": 5,
    },
    "AlphaBeta++": {
        "display_name": "AlphaBeta++ (Move Ordering)",
        "description": "Enhanced alpha-beta with killer moves & history",
        "recommended_depth": 5,
        "memory_usage": "Low",
        "speed": "4/5",
        "quality": "4/5",
        "best_for": "Fast reliable play",
        "min_depth": 3,
        "max_depth": 7,
        "heuristics": ["killer_moves", "history", "move_ordering"],
    },
    "Negamax": {
        "display_name": "Negamax (Transposition Table)",
        "description": "Simplified minimax with position caching",
        "recommended_depth": 6,
        "memory_usage": "High",
        "speed": "5/5",
        "quality": "4/5",
        "best_for": "Long games, repeated positions",
        "min_depth": 4,
        "max_depth": 8,
        "requires_tt": True,
    },
    "MTD(f)": {
        "display_name": "MTD(f) (Optimal Search)",
        "description": "Converges to exact value with null windows",
        "recommended_depth": 5,
        "memory_usage": "High",
        "speed": "3/5",
        "quality": "5/5",
        "best_for": "Precise evaluation, tough positions",
        "min_depth": 4,
        "max_depth": 7,
        "requires_tt": True,
        "iterations": 3,
    },
    "Hybrid": {
        "display_name": "Hybrid (Auto-Switching)",
        "description": "Minimax for midgame, MCTS for endgame",
        "recommended_depth": 5,
        "memory_usage": "Medium",
        "speed": "4/5",
        "quality": "5/5",
        "best_for": "Best overall performance",
        "min_depth": 4,
        "max_depth": 7,
        "switching_threshold": {
            "piece_count": 10,
            "move_count": 20,
        },
    },
}

# ========== VALUE PACK CONFIGURATIONS ==========

VALUE_PACK_DESCRIPTIONS = {
    0: {
        "name": "Standard Valuation",
        "description": "Basic piece values (R:5, C:4.5, H:3, etc)",
        "use_case": "General purpose",
    },
    1: {
        "name": "Mobility-Focused",
        "description": "Adds penalties for restricted pieces",
        "use_case": "Tactical positions",
    },
    2: {
        "name": "Advanced Position",
        "description": "Complex evaluation with game phase & piece synergy",
        "use_case": "All positions",
    },
}

# ========== RECOMMENDED SETUPS ==========

PRESETS = {
    "Quick": {
        "algorithm": "AlphaBeta++",
        "value_pack": 0,
        "depth_or_time": 3,
        "time_estimate": "0.5-1s",
        "description": "Fast moves for quick games",
    },
    "Balanced": {
        "algorithm": "Hybrid",
        "value_pack": 1,
        "depth_or_time": 5,
        "time_estimate": "5-10s",
        "description": "Good speed and strength",
    },
    "Strong": {
        "algorithm": "Negamax",
        "value_pack": 2,
        "depth_or_time": 6,
        "time_estimate": "15-25s",
        "description": "Strong play, takes time",
    },
    "Tournament": {
        "algorithm": "MTD(f)",
        "value_pack": 2,
        "depth_or_time": 6,
        "time_estimate": "20-30s",
        "description": "Best quality, slow",
    },
    "CPU Light": {
        "algorithm": "AlphaBeta++",
        "value_pack": 0,
        "depth_or_time": 4,
        "time_estimate": "2-3s",
        "description": "Low resource usage",
    },
    "CPU Heavy": {
        "algorithm": "Negamax",
        "value_pack": 2,
        "depth_or_time": 7,
        "time_estimate": "30-45s",
        "description": "Maximum strength",
    },
}

# ========== ALGORITHM SELECTION GUIDE ==========

def get_recommended_algorithm(criteria):
    """
    Get recommended algorithm based on criteria
    
    criteria = {
        'time_available': 5,          # seconds
        'cpu_cores': 4,               # number of cores
        'memory_gb': 8,               # available memory
        'position_type': 'midgame',   # opening, midgame, endgame
        'priority': 'speed'           # speed, quality, balanced
    }
    """
    
    recommendations = []
    time_available = criteria.get('time_available', 5)
    priority = criteria.get('priority', 'balanced')
    position = criteria.get('position_type', 'midgame')
    
    # Quick games (< 2 seconds)
    if time_available < 2:
        recommendations.append('AlphaBeta++')
    
    # Medium games (2-10 seconds)
    elif time_available < 10:
        if priority == 'speed':
            recommendations.append('AlphaBeta++')
        elif priority == 'quality':
            recommendations.append('Negamax')
        else:
            recommendations.append('Hybrid')
    
    # Long games (> 10 seconds)
    else:
        if priority == 'quality':
            recommendations.append('MTD(f)')
        else:
            recommendations.append('Negamax')
    
    # Position-specific
    if position == 'endgame':
        recommendations.append('MTD(f)')
    elif position == 'opening':
        recommendations.append('AlphaBeta++')
    
    return recommendations

# ========== PERFORMANCE TARGETS ==========

PERFORMANCE_TARGETS = {
    "nodes_per_second": 500000,  # Target NPS
    "evaluation_per_second": 100000,  # Evals/sec
    "max_tree_nodes": 50000,  # Max nodes in tree
    "max_memory_mb": 500,  # Max memory usage
}

# ========== HEURISTIC SETTINGS ==========

HEURISTIC_CONFIG = {
    "killer_moves": {
        "enabled": True,
        "max_killers_per_depth": 2,
        "weight": 1000,
    },
    "history_heuristic": {
        "enabled": True,
        "initial_value": 0,
        "update_on_cutoff": True,
    },
    "transposition_table": {
        "enabled": True,
        "size_entries": 1000000,
        "replacement_strategy": "always",  # always, depth, new
    },
    "move_ordering": {
        "captures_first": True,
        "checks_second": True,
        "quiet_moves": True,
    },
}

# ========== DEBUGGING & MONITORING ==========

MONITORING_CONFIG = {
    "log_searches": False,
    "log_cutoffs": False,
    "log_tt_stats": True,
    "track_nps": True,
    "profile_time": False,
    "memory_tracking": False,
}

def get_algorithm_properties(algorithm_name):
    """Get full properties of an algorithm"""
    return ALGORITHM_CONFIGS.get(algorithm_name, {})

def get_preset_config(preset_name):
    """Get preset configuration"""
    return PRESETS.get(preset_name, {})

def get_estimated_time(algorithm, depth):
    """Estimate time needed for search"""
    # Rough estimation: 10x multiplier per depth
    base_times = {
        "Minimax": 0.5,
        "AlphaBeta++": 0.8,
        "Negamax": 1.0,
        "MTD(f)": 2.0,
        "Hybrid": 1.5,
        "MCTS": 2.0,  # per second
    }
    
    base = base_times.get(algorithm, 1.0)
    return base * (1.5 ** depth)  # Rough exponential growth
