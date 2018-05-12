#
# Wrapper script
# a) start project
# b) stop project
# c) new project
# d) remove project
# e) rebuild project (docker)

from contextlib import contextmanager
import os
import sys
import shutil
from subprocess import PIPE, run, call
from string import Template

@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

def stopProject(projectName):
    print("Stopping project: " + projectName)
    with cd("projects/" + projectName):
        call(["docker", "stack", "rm", projectName])

def startProject(projectName):
    print("Starting project: " + projectName)
    with cd("projects/" + projectName):
        call(["docker", "stack", "deploy", "-c", "docker-compose.yml", projectName])

def rebuildProject(projectName):
    print("Rebuilding project: " + projectName)
    with cd("projects/" + projectName):
        call(["docker-compose", "build"])
        call(["docker-compose", "push"])
        call(["docker", "stack", "deploy", "-c", "docker-compose.yml", projectName])

def installInfra():
    print("Installing Infrastructure")
    call(["scripts/infrastructuresetup.sh"])

loop_condition = True
while loop_condition == True:
    print("#####################################")
    print("1) to start an existing project")
    print("2) to stop a running project")
    print("3) to create a new project")
    print("4) to remove a project !!WARNING!!")
    print("5) to re-deploy a project")
    print("6) Install infrastructure")
    print("7) Quit")
    print("#####################################")

    main_input = int(input("What would you like to do? "))

    if main_input == 1:
        projectName = input("Project Name: ").lower()
        startProject(projectName)
    elif main_input == 2:
        projectName = input("Project Name: ").lower()
        stopProject(projectName)
    elif main_input == 3:
        call(["python3", "./scripts/newproject.py"])
    elif main_input == 4:
        call(["python3", "./scripts/removeProject.py"])
    elif main_input == 5:
        projectName = input("Project Name: ").lower()
        rebuildProject(projectName)
    elif main_input == 6:
        installInfra()
    elif main_input == 7:
        sys.exit()
    else:
        print("Not an available option, please try again")
