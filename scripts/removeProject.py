##################
# Author: Luke Adams
# newproject deployment tool
#
##################

from contextlib import contextmanager
import os
import sys
import shutil
import subprocess
from string import Template

# Check Python version - Python 3 required
if sys.version_info[0] < 3:
    # Exit on incorrect version
    sys.exit("Error: Must be using Python 3 or higher")


@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


# Get project name variable for new deploy
print("This will REMOVE the project folder structure and Docker Containers... use with care!!")
projectName = input("Enter Project Name : ").lower()

# Check OS version information
if os.name == "posix":
    system = "Linux / Mac OS"
    subprocess.call(["./scripts/unix-managehosts.sh", "remove", projectName + ".local"])
else:
    system = "Windows"
    subprocess.call(["./scripts/win-manageghosts.ps1", "remove", projectName + ".local"])

print("Project Name: " + projectName)
print("Removing Project " + projectName)

subprocess.call(["docker", "stack", "rm", projectName])
with cd("./projects/"):
    subprocess.call(["rm", "-rf", projectName])
