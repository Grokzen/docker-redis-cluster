"""
GitHub API caching functionality for Redis Docker Cluster Build Tool.

Provides persistent caching of GitHub API responses to reduce API calls
and improve performance across multiple invocations.
"""

import os
import json
import atexit
from time import time
from cachetools import TTLCache, cached


# Cache configuration
CACHE_FILE = ".cache/github_releases.json"
cache = TTLCache(maxsize=128, ttl=1800)  # 30-minute TTL


def ensure_cache_dir():
    """Ensure the cache directory exists."""
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)


def load_cache():
    """Load cache from file if it exists."""
    try:
        with open(CACHE_FILE, 'r') as f:
            data = json.load(f)
            # Only load entries not expired
            now = time()
            for key, (value, expiry) in data.items():
                if now < expiry:
                    cache[key] = (value, expiry)
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        pass


def save_cache():
    """Save cache to file."""
    ensure_cache_dir()
    data = {key: (value, expiry) for key, (value, expiry) in cache.items()}
    with open(CACHE_FILE, 'w') as f:
        json.dump(data, f)


# Load cache on module import
load_cache()

# Save cache on exit
atexit.register(save_cache)


@cached(cache)
def fetch_github_releases_cached():
    """
    Fetch Redis releases from GitHub API with caching.

    This function is cached for 30 minutes to avoid excessive API calls.
    Returns list of valid semver release versions (excludes RCs, betas, etc.)
    Exits with error if GitHub cannot be reached or no versions found.
    """
    # Import here to avoid circular imports
    from .versions import fetch_github_releases
    return fetch_github_releases()