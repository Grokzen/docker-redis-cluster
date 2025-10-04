## 2025-10-04

* Updated Python version to 3.13 across all workflows and development environment
* Implemented comprehensive caching system using cachetools with file-based persistence for GitHub API calls (30-minute TTL)
* Modularized codebase by separating concerns into dedicated modules: cache.py for caching functionality and versions.py for version management
* Updated Python requirements: invoke>=2.2.0, requests>=2.31.0, cachetools>=5.3.0
* Created GitHub Actions workflow (test-build.yml) for automated testing and building on pull requests and non-master branches
* Refactored multiprocessing pool management to use context managers for proper resource cleanup
* Enhanced Makefile with Invoke task targets, clear-cache command, and CPU variable defaults
* Restructured README.md with separate Installation/Usage sections and updated documentation
* Fixed import issues by replacing relative imports with absolute imports for CI compatibility
* Updated dockerimage.yml workflow to build all Redis images on master branch pushes using parallel processing

## 2024-06-25

* Added 7.2.x releases and published docker images
* added 7.4-rc1 release and published
* Updated all older generations of images
* New base image that contains more updated patches etc

## 2022-12-18

* Added redis 7.0.x releases and published docker images
* Dropped redis 5.0.x releases and unpublished docker images
* Added `invoke list` command to show all possible targets you can build against

## 2021-04-13

* Dropped the availability of redis-server major versions 3.0, 3.2, 4.0 from docker.hub

## 2021-03-28

* Added versions 5.0.12, 6.0.12, 6.2.1
* Updated latest to 6.2.1

## 2021-02-28

* Rebuilt most of the build commands from Makefile into py-invoke script

## 2021-02-27

* Added versions 5.0.11, 6.0.11 & 6.2.0
* Updated latest to 6.2.0

## 2021-01-17

* Updated README with documentation regarding new github discussions feature and how to use it.
* Add new github issues template to make it easier to request features/help/support
* Add release 5.0.10
* Add support for building major version 6.2 and their RC releases
* Add release 6.0.10
* Updated latest to 6.0.10

## 2020-11-24

* Added support for IPv6 for cluster and stand-alone instances
