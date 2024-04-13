import multiprocessing
import requests

from multiprocessing import Pool
from invoke import task


latest_version_string = "7.0.10"

# Unpublished versions
version_config_mapping = []
version_config_mapping += [f"3.0.{i}" for i in range(0, 8)]
version_config_mapping += [f"3.2.{i}" for i in range(0, 14)]
version_config_mapping += [f"4.0.{i}" for i in range(0, 15)]
version_config_mapping += [f"5.0.{i}" for i in range(0, 13)]

# Published versions
version_config_mapping += [f"6.0.{i}" for i in range(0, 19)]
version_config_mapping += [f"6.2.{i}" for i in range(0, 12)]
version_config_mapping += [f"7.0.{i}" for i in range(0, 11)]


def version_name_to_version(version):
    """
    Helper method that returns correct versions if you specify either
     - all
     - latest

    or it will filter your chosen version based on what you inputed as version argument
    """
    if version == "all":
        return version_config_mapping
    elif version == "latest":
        return [latest_version_string]
    else:
        return filter_versions(version)


def get_pool_size(cpu_from_cli):
    if cpu_from_cli:
        pool_size = int(cpu_from_cli)
    else:
        pool_size = multiprocessing.cpu_count() - 1

    print(f"Configured multiprocess pool size: {pool_size}")
    return pool_size


def filter_versions(desired_version):
    result = []

    for version in version_config_mapping:
        if version.startswith(desired_version):
            result.append(version)

    return result


def _docker_pull(config):
    """
    Internal multiprocess method to run docker pull command
    """
    c, version = config
    print(f" -- Starting docker pull for version : {version}")
    pull_command = f"docker pull grokzen/redis-cluster:{version}"
    c.run(pull_command)


def _docker_build(config):
    """
    Internal multiprocess method to run docker build command
    """
    c, version = config
    print(f" -- Starting docker build for version : {version}")
    build_command = f"docker build --build-arg redis_version={version} -t grokzen/redis-cluster:{version} ."
    c.run(build_command)


def _docker_push(config):
    """
    Internal multiprocess method to run docker push command
    """
    c, version = config
    print(f" -- Starting docker push for version : {version}")
    build_command = f"docker push grokzen/redis-cluster:{version}"
    c.run(build_command)


@task
def pull(c, version, cpu=None):
    print(f" -- Docker pull version docker-hub : {version}")

    pool = Pool(get_pool_size(cpu))
    pool.map(
        _docker_pull,
        [
            [c, version]
            for version in version_name_to_version(version)
        ],
    )


@task
def build(c, version, cpu=None):
    print(f" -- Docker building version : {version}")

    pool = Pool(get_pool_size(cpu))
    pool.map(
        _docker_build,
        [
            [c, version]
            for version in version_name_to_version(version)
        ],
    )


@task
def push(c, version, cpu=None):
    print(f" -- Docker push version to docker-hub : {version}")

    pool = Pool(get_pool_size(cpu))
    pool.map(
        _docker_push,
        [
            [c, version]
            for version in version_name_to_version(version)
        ],
    )


@task
def list(c):
    from pprint import pprint
    pprint(version_config_mapping, indent=2)


@task
def list_releases(c):
    releases = []

    for page in range(1, 5):
        data = requests.get("https://api.github.com/repos/redis/redis/releases", params={"page": int(page)})

        if data.status_code == 200:
            for release in data.json():
                r = release["name"]

                if "rc" in r or r.startswith("5"):
                    pass
                else:
                    releases.append(r)
        else:
            print("Error, stopping")

    for released_version in releases:
        if released_version in version_config_mapping:
            print(f"Release found - {released_version}")
        else:
            print(f"NOT found - {released_version}")
