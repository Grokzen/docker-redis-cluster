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
import sys
from multiprocessing import Pool
from invoke import task
from invoke.context import Context

from cache import fetch_github_releases_cached
from versions import (
    generate_version_ranges,
    get_latest_version,
    initialize_version_data,
    version_name_to_version,
    version_sort_key,
)
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
    
    Fetches Redis releases from GitHub API (using cache if available) and displays comprehensive
    information about available versions, latest releases, and the dynamic
    version loading process.
        
    Examples:
        $ invoke list-releases
        
    Output:
        Shows GitHub releases, dynamic version loading status, and statistics.
        
    Note:
        Uses cached data when available (30 minute TTL).
        Requires internet connection to access GitHub API.
        API rate limits may apply for unauthenticated requests.
    """
    print("Fetching GitHub releases...")
    print("=" * 60)
    
    # Fetch releases (cached if available)
    fresh_releases = fetch_github_releases_cached()
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
