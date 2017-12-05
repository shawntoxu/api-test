sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
echo 'deb https://apt.dockerproject.org/repo ubuntu-trusty main' >> /etc/apt/sources.list.d/docker.list
apt-get update 

#show all version
 apt-cache policy docker-engine

#install 1.10
apt-get install docker-engine=1.10.0-0~trusty 

