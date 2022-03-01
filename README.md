
# Docker Instructions for Kali on ARM
Help on installing Kali Linux on an M1 Mac

## **Overview**

Welcome to the Docker installation tutorial for ARM users seeking to install the x86 version of Kali on their ARM based system. Note we are focusing on the Macintosh that provides a hardware accelerated binary translator for converting non-ARM instructions to ARM. Other systems might be much slower using these methods. We need to set up the environment for this programming assignment. 

This tutorial provides instructions to install Docker on your ARM based Mac, build a Docker image from our Dockerfile, and run the Docker image in a new container.

**Objectives**

Upon completing this tutorial, you shall be able to:

-   Set up the Docker installation
    
-   Build Docker image from Dockerfile
    
-   Run the Docker image in a new container
    
-   Delete a Docker image
    

## **Requirements and Installation**

Install **Docker Desktop** on your computer

1.  go to [https://docs.docker.com/docker-for-mac/install/](https://docs.docker.com/docker-for-mac/install/)
    
2.  follow the "Install and run Docker Desktop on Mac" instructions
	- Open a terminal window and run ` softwareupdate --install-rosetta
`
	- Agree to the terms by hitting `a`
	- Open the .dmg file and drag docker to your applications folder.
	- Open the Docker.app file from within you applications folder, it'll install and then agree to the terms. Note: you will use docker from the CLI, i.e. command-line going forward.
    
    

## Build Docker image from Dockerfile

### Option 1: Build from scratch
**step1:** Pull the latest Kali release:
`$ docker pull kalilinux/kali-rolling`

**step2**: Start the kali image:
	`$ docker run --tty --interactive kalilinux/kali-rolling /bin/bash`

**step3:** Time to install tools!
-  **Advanced:** 
`root@<some-sha1>: apt update && apt -y install kali-linux-headless`
Note: this will take some time!

- **Beginner:**
`root@<some-sha1>: apt update`
`root@<some-sha1>: apt dist-upgrade`
`root@<some-sha1>: apt autoremove`  
`root@<some-sha1>: apt clean`

	Now install the Top 10 tools to start:
	`apt install kali-tools-top10`
	`apt install kali-linux-arm`

To exit the virtual machine, use **Ctrl+D;** Please note that once you exit the virtual machine, the changes that you made inside the virtual machine will NOT remain when you run that Docker image in a new container. Instead, the changes will be made to the existing Docker container. You could start the stopped container and attach to it using:
`docker start [OPTIONS] CONTAINER [CONTAINER...]`
`docker exec -it CONTAINER_ID /bin/bash`

**I suggest typing just typing `exit` to exit the Docker instance of Kali.**

**step4**: Let's set a friendlier name form the docker image!
`docker ps -a`

Then look for the container name:
| CONTAINER ID	| IMAGE  |	COMMAND | CREATED | STATUS |PORTS  | NAMES |
| --- | --- | --- | --- | --- | --- | --- |
| 2a08d58bcfa8 | kalilinux/kali-rolling | "/bin/bash" | About a minute ago | Exited (0) 2 seconds ago | thirsty_snyder` |

Let's change the name:
`docker commit <CONTAINER ID> my-kali` where <CONTAINER ID> would be `2a08d58bcfa8` in the example.

**You can now run the container as `docker run -ti my-kali /bin/bash` going forward!**

Using metasploit? Then you need persistance storage! In that case please run the docker container as:
`docker run -ti --rm --mount src=kali-root,dst=/root --mount src=kali-postgres,dst=/var/lib/postgresql my-kali`

**step5**: Power Docker down:
Type `docker-compose down` to shutdown docker.

### Option 2: The easy way (includes wordpress)
```bash
git clone https://github.com/LifeBringer/Docker-Instructions-M1-Kali.git
DOCKER_BUILDKIT=1 docker compose build
mkdir kaliFolder
```

#### Run Wordpress + mysql and Kali containers

```bash
  docker compose up -d
  ID=$(docker ps -a | grep my-kali | gawk '{print $1}') && docker exec -it $ID bash
  ```
- On both the host machine and on the Kali terminal, the WordPress website is hosted at http://localhost:8080

- Type `exit` to exit the Kali bash shell and to shutdown all running containers use, `docker compose down`

### Changing Wordpress versions:
All credit too: https://github.com/0xrutvij/wpVSkali
Within your docker contianer, install the requirements file for python3 before proceeding `pip3 install -r requirements.txt`
 
 For changing WordPress versions, use the not-wp-dis.py script, usage is as follows:
  ```bash
  Modify Compose File.

  Usage:
    not-wp-dis.py [--wordpress=<ver>] [--wpPort=<port>]
    not-wp-dis.py (-h | --help)
    not-wp-dis.py (-v | --version)
    not-wp-dis.py (--listWpVer)

  Options:
    -h --help            Show this screen.
    -v --version         Show version.
    --wordpress=<ver>    Wordpress version to use [default: latest].
    --wpPort=<port>      Port at which the Wordpress website is served [default: 8080].
    --listWpVer          List Wordpress versions available.
  ```

## Delete a Docker image

If your Docker machine has too many Docker images, you may want to delete unused images.

To list the Docker images and their 'CONTAINER ID", run:
`$ docker images`

To delete a docker image with "CONTAINER ID": 2a08d58bcfa8, run:
`$ docker rmi 2a08d58bcfa8`

For more information about Docker, please visit:
[https://docs.docker.com/engine/reference/commandline/docker/](https://docs.docker.com/engine/reference/commandline/docker/)
