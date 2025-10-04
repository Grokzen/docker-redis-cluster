"""
Enhanced Redis Docker Cluster Build Tool using Python Invoke

This module provides an improved CLI interface for building, pulling, and pushing
Redis cluster Docker images with enhanced documentation and dictionary-based
parameter handling.

Usage Examples:
    invoke pull --version latest
    invoke build --version 7.2 --cpu 4
    invoke push --version all
    invoke list
    invoke list-releases
"""

import multiprocessing
import requests
import re
import sys
from multiprocessing import Pool
from invoke import task
from invoke.context import Context
from contextlib import contextmanager


@contextmanager
def managed_pool(pool_size):
    """
    Context manager for multiprocessing Pool that ensures proper cleanup.
    
    Automatically handles pool.close() and pool.join() when exiting the context.
    """
    pool = Pool(pool_size)
    try:
        yield pool
    finally:
        pool.close()
        pool.join()


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
    Returns tuple of (version_mapping, latest_version)
    """
    print("Fetching Redis releases from GitHub...")
    github_releases = fetch_github_releases()
    
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


def get_pool_size(cpu_from_cli):
    """
    Determine optimal multiprocessing pool size.
    
    Calculates the number of worker processes to use for parallel operations.
    If no CPU count is specified, uses system CPU count minus 1 to avoid
    overwhelming the system.
    """
    if cpu_from_cli:
        pool_size = int(cpu_from_cli)
    else:
        pool_size = multiprocessing.cpu_count() - 1

    print(f"Configured multiprocess pool size: {pool_size}")
    return pool_size


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


def _docker_pull(config):
    """
    Internal multiprocess worker for Docker pull operations.
    
    Executes docker pull command for a specific Redis cluster version
    in a separate process for parallel execution.
    
    Config dictionary should contain:
    - 'context': Invoke context object
    - 'version': Redis version to pull
    """
    context = config['context']
    version = config['version']
    
    print(f" -- Starting docker pull for version: {version}")
    pull_command = f"docker pull grokzen/redis-cluster:{version}"
    
    try:
        context.run(pull_command)
        print(f" -- Successfully pulled version: {version}")
    except Exception as e:
        print(f" -- Error pulling version {version}: {e}")


def _docker_build(config):
    """
    Internal multiprocess worker for Docker build operations.
    
    Executes docker build command for a specific Redis cluster version
    in a separate process for parallel execution.
    
    Config dictionary should contain:
    - 'context': Invoke context object
    - 'version': Redis version to build
    """
    context = config['context']
    version = config['version']
    
    print(f" -- Starting docker build for version: {version}")
    build_command = f"docker build --build-arg redis_version={version} -t grokzen/redis-cluster:{version} ."
    
    try:
        context.run(build_command)
        print(f" -- Successfully built version: {version}")
    except Exception as e:
        print(f" -- Error building version {version}: {e}")


def _docker_push(config):
    """
    Internal multiprocess worker for Docker push operations.
    
    Executes docker push command for a specific Redis cluster version
    in a separate process for parallel execution.
    
    Config dictionary should contain:
    - 'context': Invoke context object
    - 'version': Redis version to push
    """
    context = config['context']
    version = config['version']
    
    print(f" -- Starting docker push for version: {version}")
    push_command = f"docker push grokzen/redis-cluster:{version}"
    
    try:
        context.run(push_command)
        print(f" -- Successfully pushed version: {version}")
    except Exception as e:
        print(f" -- Error pushing version {version}: {e}")


@task(help={
    'version': 'Redis version to pull. Options: "all", "latest", or specific version pattern (e.g., "7.2")',
    'cpu': 'Number of CPU cores to use for parallel processing (default: system cores - 1)'
})
def pull(c, version, cpu=None):
    """
    Pull Redis cluster Docker images from Docker Hub.
    
    Downloads pre-built Redis cluster images for the specified version(s)
    using parallel processing for improved performance.
        
    Examples:
        Pull latest stable version:
        $ invoke pull --version latest
        
        Pull all 7.2.x versions:
        $ invoke pull --version 7.2
        
        Pull all versions using 4 CPU cores:
        $ invoke pull --version all --cpu 4
        
    Note:
        Requires Docker to be installed and accessible via command line.
        Large version sets may take considerable time to complete.
    """
    print(f" -- Docker pull from Docker Hub for version: {version}")
    
    # Initialize version data from GitHub
    version_mapping, latest_version = initialize_version_data()
    
    versions = version_name_to_version(version, version_mapping, latest_version)
    if not versions:
        print(f"Error: No versions found matching '{version}'")
        print("Use 'invoke list' to see available versions")
        return
        
    print(f" -- Found {len(versions)} version(s) to pull")

    configs = [
        {'context': c, 'version': v} 
        for v in versions
    ]
    
    with managed_pool(get_pool_size(cpu)) as pool:
        pool.map(_docker_pull, configs)
        print(f" -- Completed pulling {len(versions)} version(s)")


@task(help={
    'version': 'Redis version to build. Options: "all", "latest", or specific version pattern (e.g., "7.2")',
    'cpu': 'Number of CPU cores to use for parallel processing (default: system cores - 1)'
})
def build(c, version, cpu=None):
    """
    Build Redis cluster Docker images locally.
    
    Compiles Redis cluster Docker images for the specified version(s)
    using parallel processing. Requires a Dockerfile in the current directory.
        
    Examples:
        Build latest stable version:
        $ invoke build --version latest
        
        Build all 6.2.x versions:
        $ invoke build --version 6.2
        
        Build specific version with custom CPU count:
        $ invoke build --version 7.2.5 --cpu 2
        
    Note:
        Requires Docker and a properly configured Dockerfile.
        Building all versions can take several hours and significant disk space.
    """
    print(f" -- Docker building version: {version}")
    
    # Initialize version data from GitHub
    version_mapping, latest_version = initialize_version_data()
    
    versions = version_name_to_version(version, version_mapping, latest_version)
    if not versions:
        print(f"Error: No versions found matching '{version}'")
        print("Use 'invoke list' to see available versions")
        return
        
    print(f" -- Found {len(versions)} version(s) to build")

    configs = [
        {'context': c, 'version': v} 
        for v in versions
    ]
    
    with managed_pool(get_pool_size(cpu)) as pool:
        pool.map(_docker_build, configs)
        print(f" -- Completed building {len(versions)} version(s)")


@task(help={
    'version': 'Redis version to push. Options: "all", "latest", or specific version pattern (e.g., "7.2")',
    'cpu': 'Number of CPU cores to use for parallel processing (default: system cores - 1)'
})
def push(c, version, cpu=None):
    """
    Push Redis cluster Docker images to Docker Hub.
    
    Uploads locally built Redis cluster images to Docker Hub registry
    using parallel processing for improved performance.
        
    Examples:
        Push latest version:
        $ invoke push --version latest
        
        Push all 7.0.x versions:
        $ invoke push --version 7.0
        
        Push all versions with limited parallelism:
        $ invoke push --version all --cpu 2
        
    Note:
        Requires Docker Hub authentication and push permissions.
        Images must be built locally before pushing.
    """
    print(f" -- Docker push to Docker Hub for version: {version}")
    
    # Initialize version data from GitHub
    version_mapping, latest_version = initialize_version_data()
    
    versions = version_name_to_version(version, version_mapping, latest_version)
    if not versions:
        print(f"Error: No versions found matching '{version}'")
        print("Use 'invoke list' to see available versions")
        return
        
    print(f" -- Found {len(versions)} version(s) to push")

    configs = [
        {'context': c, 'version': v} 
        for v in versions
    ]
    
    with managed_pool(get_pool_size(cpu)) as pool:
        pool.map(_docker_push, configs)
        print(f" -- Completed pushing {len(versions)} version(s)")


@task(help={})
def list(c):
    """
    Display all available Redis versions.
    
    Shows a comprehensive list of all Redis versions that can be built,
    including both published and unpublished versions. Useful for
    identifying available version patterns.
        
    Examples:
        $ invoke list
        
    Output:
        Displays formatted list of all available Redis versions
        organized by major.minor version groups.
    """
    from pprint import pprint
    
    print("Available Redis versions:")
    print("=" * 50)
    
    # Initialize version data from GitHub
    version_mapping, latest_version = initialize_version_data()
    
    # Group versions by major.minor for better readability
    version_groups = {}
    for version in version_mapping:
        if "rc" in version:
            key = "Release Candidates"
        else:
            parts = version.split('.')
            if len(parts) >= 2:
                key = f"{parts[0]}.{parts[1]}.x"
            else:
                key = "Other"
        
        if key not in version_groups:
            version_groups[key] = []
        version_groups[key].append(version)
    
    for group, versions in sorted(version_groups.items()):
        print(f"\n{group}:")
        pprint(versions, indent=2, width=100)
    
    print(f"\nTotal versions available: {len(version_mapping)}")
    print(f"Latest stable version: {latest_version}")


@task(name='list-releases', help={})
def list_releases(c):
    """
    Display GitHub releases and show dynamic version loading status.
    
    Fetches fresh Redis releases from GitHub API and displays comprehensive
    information about available versions, latest releases, and the dynamic
    version loading process.
        
    Examples:
        $ invoke list-releases
        
    Output:
        Shows GitHub releases, dynamic version loading status, and statistics.
        
    Note:
        Requires internet connection to access GitHub API.
        API rate limits may apply for unauthenticated requests.
    """
    print("Fetching fresh GitHub releases...")
    print("=" * 60)
    
    # Fetch fresh releases directly (this will exit on error)
    fresh_releases = fetch_github_releases()
    latest_version = get_latest_version(fresh_releases)
    current_generated = generate_version_ranges(fresh_releases)
    
    print(f"✓ Successfully fetched {len(fresh_releases)} valid releases from GitHub")
    print(f"✓ Latest version found: {latest_version}")
    
    # Show version range statistics
    major_minor_stats = {}
    for version in fresh_releases:
        parts = version.lstrip('v').split('.')
        if len(parts) >= 2:
            key = f"{parts[0]}.{parts[1]}.x"
            if key not in major_minor_stats:
                major_minor_stats[key] = 0
            major_minor_stats[key] += 1
    
    print(f"\nVersion Series Statistics:")
    print("-" * 30)
    for series, count in sorted(major_minor_stats.items(), key=lambda x: version_sort_key(x[0])):
        print(f"{series:10} : {count:3} releases")
    
    # Show recent releases (last 10)
    print(f"\nRecent Releases (Latest 10):")
    print("-" * 30)
    recent_releases = sorted(fresh_releases, key=lambda x: version_sort_key(x), reverse=True)[:10]
    for i, version in enumerate(recent_releases, 1):
        marker = "← LATEST" if i == 1 else ""
        print(f"{i:2}. {version} {marker}")
    
    print(f"\nDynamic Version Generation:")
    print("-" * 30)
    print(f"GitHub releases found    : {len(fresh_releases)}")
    print(f"Generated version ranges : {len(current_generated)}")
    print(f"Latest version detected  : {latest_version}")
    print(f"Total available versions : {len(current_generated)}")
