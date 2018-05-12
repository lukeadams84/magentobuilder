# Cross Platform Magento 1/2 Docker Environment Builder

Python3 Project to allow quick build of custom Magento environments for Docker Swarm. Projects are created automatically, and need to stay in the projects folder for the automated start, stop, rebuild etc to work. 

## Getting Started

Clone the repository into your chosen location. This is recommended to be somewhere in your documents or working locations.

### Prerequisites

You need to have the latest Docker CE installed for Windows, Mac or Linux. And Python3 installed into your PATH. Depending on how you installed Python, it might be available as python script or as python3 script

```
Python 3 installed as python

python starthere.py

Python 3 installed as python3

python3 starthere.py
```

### Installing

Clone the REPO, then run python3 starthere.py

```
python3 starthere.py
#####################################
1) to start an existing project
2) to stop a running project
3) to create a new project
4) to remove a project !!WARNING!!
5) to re-deploy a project
6) Install infrastructure
7) Quit
#####################################
What would you like to do?
```

First, make sure you have Docker running, then run option 6 to create the swarm, internal and proxy networks and to set up the dockerhub login.

You will need to know your dockerhub login details as they now require authentication to pull repositories.

## Authors

* **Luke Adams** - *Initial work*
