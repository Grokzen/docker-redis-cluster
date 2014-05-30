## Docker support

To make it easier to test this library there is an Dockerfile that can be used to install and run an entire redis cluster.

The cluster is 6 redis instances running with 3 master & 3 slaves.

It will allways run on the latest commit in the 3.0 branch of redis git repo (https://github.com/antirez/redis). To change this, change the git clone command inside Dockerfile.

How to setup docker and start the cluster image.

- Install lxc-docker on your system (I currently use Docker version 0.7.1, build 88df052) (Instructions can be found at: http://docs.docker.io/en/latest/installation/)
- Naviaget to root of this project
- Run 'make docker-build'
- Run 'make docker-run' or 'make docker-run-d' if you want to run the image in daemon (For interactive/debug mode run 'make docker-run-interactive')
- redis-trib.rb will prompt your for a question to create the cluster, type 'yes' and press enter.
- Test the connection by running either 'redis-cli -p 7000' or 'python example.py'
