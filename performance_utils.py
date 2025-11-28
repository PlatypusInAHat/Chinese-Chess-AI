"""
Performance Optimization Utilities for Chinese Chess AI
Contains caching, profiling, and performance monitoring tools
"""

import time
from functools import wraps
from collections import OrderedDict
import gc
from optimization_config import (
    CACHE_SIZE, 
    GARBAGE_COLLECTION_INTERVAL,
    ENABLE_PROFILING,
    PROFILE_OUTPUT_FILE
)


class LRUCache:
    """Custom LRU Cache implementation for board states"""
    
    def __init__(self, maxsize=CACHE_SIZE):
        self.maxsize = maxsize
        self.cache = OrderedDict()
        self.hits = 0
        self.misses = 0
    
    def get(self, key):
        if key in self.cache:
            self.hits += 1
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            return self.cache[key]
        self.misses += 1
        return None
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.maxsize:
            # Remove least recently used
            self.cache.popitem(last=False)
    
    def get_stats(self):
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'size': len(self.cache)
        }
    
    def clear(self):
        self.cache.clear()
        self.hits = 0
        self.misses = 0


class TranspositionTable:
    """Transposition table for storing computed game states"""
    
    def __init__(self, maxsize=100000):
        self.table = {}
        self.maxsize = maxsize
        self.hits = 0
        self.misses = 0
    
    def store(self, board_hash, depth, value, flag):
        """Store (hash, depth, value, flag) in transposition table
        flag: 'EXACT', 'LOWER', 'UPPER'
        """
        if len(self.table) >= self.maxsize:
            # Simple eviction: remove oldest entry
            self.table.pop(next(iter(self.table)))
        
        self.table[board_hash] = {'depth': depth, 'value': value, 'flag': flag}
    
    def lookup(self, board_hash, depth):
        """Lookup value in transposition table"""
        if board_hash in self.table:
            entry = self.table[board_hash]
            if entry['depth'] >= depth:
                self.hits += 1
                return entry['value'], entry['flag']
        self.misses += 1
        return None, None
    
    def clear(self):
        self.table.clear()
        self.hits = 0
        self.misses = 0


class PerformanceMonitor:
    """Monitor AI performance metrics"""
    
    def __init__(self):
        self.metrics = {
            'nodes_evaluated': 0,
            'moves_generated': 0,
            'cache_hits': 0,
            'total_time': 0
        }
        self.iteration_count = 0
    
    def start_timer(self):
        self.start_time = time.time()
    
    def end_timer(self):
        elapsed = time.time() - self.start_time
        self.metrics['total_time'] += elapsed
        return elapsed
    
    def record_node_evaluation(self, count=1):
        self.metrics['nodes_evaluated'] += count
    
    def record_move_generation(self, count=1):
        self.metrics['moves_generated'] += count
    
    def get_nps(self):
        """Get nodes per second"""
        if self.metrics['total_time'] > 0:
            return self.metrics['nodes_evaluated'] / self.metrics['total_time']
        return 0
    
    def print_stats(self):
        print("\n" + "="*50)
        print("PERFORMANCE STATISTICS")
        print("="*50)
        print(f"Nodes Evaluated: {self.metrics['nodes_evaluated']:,}")
        print(f"Moves Generated: {self.metrics['moves_generated']:,}")
        print(f"Total Time: {self.metrics['total_time']:.2f}s")
        print(f"Nodes Per Second: {self.get_nps():.0f}")
        print("="*50 + "\n")


def profile_function(func):
    """Decorator to profile function execution time"""
    if not ENABLE_PROFILING:
        return func
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        
        with open(PROFILE_OUTPUT_FILE, 'a') as f:
            f.write(f"{func.__name__}: {elapsed:.4f}s\n")
        
        return result
    return wrapper


class MemoryOptimizer:
    """Optimize memory usage during AI computation"""
    
    gc_counter = 0
    
    @classmethod
    def periodic_cleanup(cls):
        """Perform periodic garbage collection"""
        cls.gc_counter += 1
        if cls.gc_counter >= GARBAGE_COLLECTION_INTERVAL:
            gc.collect()
            cls.gc_counter = 0
    
    @staticmethod
    def optimize_board_representation(board):
        """Convert board to more efficient representation"""
        # Can be optimized further by using numpy arrays or bit manipulation
        return tuple(tuple(row) for row in board)
    
    @staticmethod
    def get_memory_usage():
        """Get current memory usage in MB"""
        import psutil
        import os
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024


# Global instances
board_cache = LRUCache(CACHE_SIZE)
transposition_table = TranspositionTable()
performance_monitor = PerformanceMonitor()
