"""utils/cache.py
Simple in-memory cache implementation with TTL support.
Thread-safe for concurrent access.
"""

import time
import threading
from typing import Any, Optional, Dict
from dataclasses import dataclass


@dataclass
class CacheEntry:
    """Cache entry with value and expiration time."""
    value: Any
    expires_at: float


class SimpleCache:
    """Thread-safe in-memory cache with TTL support."""
    
    def __init__(self):
        self._cache: Dict[str, CacheEntry] = {}
        self._lock = threading.Lock()
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """
        Set a cache entry with TTL.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (default: 1 hour)
        """
        expires_at = time.time() + ttl
        entry = CacheEntry(value=value, expires_at=expires_at)
        
        with self._lock:
            self._cache[key] = entry
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get a cache entry if it exists and hasn't expired.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        with self._lock:
            entry = self._cache.get(key)
            
            if entry is None:
                return None
            
            # Check if expired
            if time.time() > entry.expires_at:
                del self._cache[key]
                return None
            
            return entry.value
    
    def delete(self, key: str) -> None:
        """
        Delete a cache entry.
        
        Args:
            key: Cache key
        """
        with self._lock:
            self._cache.pop(key, None)
    
    def clear(self) -> None:
        """Clear all cache entries."""
        with self._lock:
            self._cache.clear()
    
    def cleanup_expired(self) -> int:
        """
        Remove all expired entries.
        
        Returns:
            Number of entries removed
        """
        current_time = time.time()
        removed_count = 0
        
        with self._lock:
            expired_keys = [
                key for key, entry in self._cache.items()
                if current_time > entry.expires_at
            ]
            
            for key in expired_keys:
                del self._cache[key]
                removed_count += 1
        
        return removed_count


# Global cache instance
cache = SimpleCache()
