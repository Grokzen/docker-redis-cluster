import multiprocessing
from multiprocessing import Pool
from invoke import task


latest_version_string = "6.2.0"

version_config_mapping = [
    "3.0.0",
    "3.0.1",
    "3.0.2",
    "3.0.3",
    "3.0.4",
    "3.0.5",
    "3.0.6",
    "3.0.7",

    "3.2.0",
    "3.2.1",
    "3.2.2",
    "3.2.3",
    "3.2.4",
    "3.2.5",
    "3.2.6",
    "3.2.7",
    "3.2.8",
    "3.2.9",
    "3.2.10",
    "3.2.11",
    "3.2.12",
    "3.2.13",

    "4.0.0",
    "4.0.1",
    "4.0.2",
    "4.0.3",
    "4.0.4",
    "4.0.5",
    "4.0.6",
    "4.0.7",
    "4.0.8",
    "4.0.9",
    "4.0.10",
    "4.0.11",
    "4.0.12",
    "4.0.13",
    "4.0.14",

    "5.0.0",
    "5.0.1",
    "5.0.2",
    "5.0.3",
    "5.0.4",
    "5.0.5",
    "5.0.6",
    "5.0.7",
    "5.0.8",
    "5.0.9",
    "5.0.10",
    "5.0.11",

    "6.0.0",
    "6.0.1",
    "6.0.2",
    "6.0.3",
    "6.0.4",
    "6.0.5",
    "6.0.6",
    "6.0.7",
    "6.0.8",
    "6.0.9",
    "6.0.10",
    "6.0.11",

    "6.2-rc1",
    "6.2-rc2",
    "6.2.0",
]


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
        _docker_build,
        [
            [c, version]
            for version in version_name_to_version(version)
        ],
    )
