"""
Version management functionality for Redis Docker Cluster Build Tool.

Handles fetching, filtering, and processing Redis version information
from GitHub API responses.
"""

import requests
import re
import sys


def fetch_github_releases():
    """
    Fetch Redis releases from GitHub API and filter valid semver versions.

    Returns list of valid semver release versions (excludes RCs, betas, etc.)
    Exits with error if GitHub cannot be reached or no versions found.
    """
    releases = []

    try:
        for page in range(1, 10):  # Fetch more pages to get comprehensive history
            response = requests.get(
                "https://api.github.com/repos/redis/redis/releases",
                params={"page": page, "per_page": 100},
                timeout=30
            )

            if response.status_code == 200:
                page_releases = response.json()
                if not page_releases:  # No more releases
                    break

                for release in page_releases:
                    tag_name = release.get("tag_name", "")
                    release_name = release.get("name", "")

                    # Use tag_name primarily, fallback to name
                    version = tag_name if tag_name else release_name

                    # Filter valid semver versions (exclude RCs, betas, alphas, etc.)
                    if is_valid_semver_release(version):
                        releases.append(version)

            elif response.status_code == 403:
                print("Error: GitHub API rate limit exceeded. Please try again later.")
                sys.exit(1)
            else:
                print(f"Error: GitHub API returned status {response.status_code}")
                sys.exit(1)

    except requests.exceptions.RequestException as e:
        print(f"Error: Cannot connect to GitHub API: {e}")
        sys.exit(1)

    if not releases:
        print("Error: No valid Redis versions found on GitHub")
        sys.exit(1)

    return sorted(set(releases), key=lambda x: version_sort_key(x))


def is_valid_semver_release(version):
    """
    Check if a version string is a valid semantic version release.

    Excludes pre-release versions (rc, alpha, beta, etc.)
    """
    # Remove 'v' prefix if present
    clean_version = version.lstrip('v')

    # Pattern for semantic versioning (major.minor.patch)
    semver_pattern = r'^(\d+)\.(\d+)\.(\d+)$'

    # Exclude pre-release versions (rc, alpha, beta, etc.)
    exclude_patterns = [
        r'rc\d*',     # release candidates
        r'alpha',     # alpha versions
        r'beta',      # beta versions
        r'pre',       # pre-release
        r'dev',       # development
        r'unstable',  # unstable
        r'-',         # any version with dash (pre-release indicator)
    ]

    # Check if it matches semver pattern
    if not re.match(semver_pattern, clean_version):
        return False

    # Check if it contains any excluded patterns
    for pattern in exclude_patterns:
        if re.search(pattern, clean_version, re.IGNORECASE):
            return False

    return True


def version_sort_key(version):
    """
    Create a sort key for version strings for proper version ordering.
    """
    clean_version = version.lstrip('v')
    parts = clean_version.split('.')

    try:
        return tuple(int(part) for part in parts)
    except ValueError:
        # Fallback for non-numeric parts
        return (0, 0, 0)


def generate_version_ranges(github_releases):
    """
    Generate comprehensive version ranges based on GitHub releases.

    Creates complete version mapping including intermediate versions.
    """
    version_mapping = []

    # Group releases by major.minor
    major_minor_groups = {}
    for version in github_releases:
        clean_version = version.lstrip('v')
        parts = clean_version.split('.')

        if len(parts) >= 2:
            try:
                major = int(parts[0])
                minor = int(parts[1])
                patch = int(parts[2]) if len(parts) > 2 else 0

                key = f"{major}.{minor}"
                if key not in major_minor_groups:
                    major_minor_groups[key] = []
                major_minor_groups[key].append(patch)
            except ValueError:
                continue

    # Generate ranges for each major.minor group
    for major_minor, patches in major_minor_groups.items():
        max_patch = max(patches)

        # Generate all versions from 0 to max_patch
        for patch in range(0, max_patch + 1):
            version_mapping.append(f"{major_minor}.{patch}")

    return sorted(set(version_mapping), key=lambda x: version_sort_key(x))


def get_latest_version(versions):
    """
    Get the latest version from a list of versions.
    """
    if not versions:
        print("Error: No versions provided to determine latest")
        sys.exit(1)

    return max(versions, key=lambda x: version_sort_key(x))


def initialize_version_data():
    """
    Initialize version data by fetching from GitHub.

    Uses cached GitHub release data when available (30 minute TTL).

    Returns tuple of (version_mapping, latest_version)
    """
    from .cache import fetch_github_releases_cached

    github_releases = fetch_github_releases_cached()

    version_mapping = generate_version_ranges(github_releases)
    latest_version = get_latest_version(github_releases)

    print(f"Successfully loaded {len(version_mapping)} versions from GitHub")
    print(f"Latest version detected: {latest_version}")

    return version_mapping, latest_version


def version_name_to_version(version, version_mapping, latest_version):
    """
    Convert version specification to actual version list.

    Handles special version keywords and filters versions based on user input.
    - "all": Returns all available versions
    - "latest": Returns only the latest stable version
    - Specific version pattern: Returns matching versions (e.g., "7.2" returns all 7.2.x versions)
    """
    if version == "all":
        return version_mapping
    elif version == "latest":
        return [latest_version]
    else:
        return filter_versions(version, version_mapping)


def filter_versions(desired_version, version_mapping):
    """
    Filter available versions based on prefix matching.

    Searches through all available Redis versions and returns those
    that start with the specified version pattern.
    """
    result = []

    for version in version_mapping:
        if version.startswith(desired_version):
            result.append(version)

    return result