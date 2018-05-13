##################
# Author: Luke Adams
# newproject deployment tool
#
##################

from contextlib import contextmanager
import os
import sys
import shutil
from subprocess import PIPE, run, call
from string import Template

# Magento version files - if you change them - ensure the replacement .tar file is in .magento/srcfiles directory
magento22 = "magento2-2.2.4.tar.gz"
magento21 = "magento2-2.1.13.tar.gz"
magento20 = "magento2-2.0.18.tar"
magento1 = "magento-1.9.3.7.tar"

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

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            print('Copying {0}'.format(item))
            shutil.copytree(s, d, symlinks, ignore)
        else:
            print('Copying {0}'.format(item))
            shutil.copy2(s, d)

# Function to update the templated compose file with project name variables
def composeReplace():
    filein = open('.magento/compose/magento-' + magentoVersion.split(".")[0] + '/docker-compose.yml')
    dictionary = {'pjn': projectName}
    src = Template(filein.read())
    result = src.substitute(dictionary)
    newFile = open("./projects/" + projectName + '/docker-compose.yml', "w+")
    newFile.write(result)
    newFile.close()

def binReplace(fn):
    filein = open('.magento/compose/magento-' + magentoVersion.split(".")[0] + '/bin/' + fn)
    dictionary = {'pjnfpm': projectName + '_phpfpm', 'pjn': projectName, 'pjndb': projectName + '_db'}
    src = Template(filein.read())
    result = src.substitute(dictionary)
    newFile = open("./projects/" + projectName + '/bin/' + fn, "w+")
    newFile.write(result)
    newFile.close()


# Get project name variable for new deploy
projectName = input("Enter Project Name : ").lower()
magentoVersion = input("Enter Magento Version (1|2.0|2.1|2.2): ")
if magentoVersion == '2.2':
    phpVer = input("Enter PHP Version (7.1): ")
else:
    phpVer = input("Enter PHP Version (5.6|7.0): ")

# Check OS version information
if os.name == "posix":
    system = "Linux / Mac OSX"
    call(["./scripts/unix-managehosts.sh", "add", projectName + ".local"])
else:
    system = "Windows"
    call(["./scripts/win-manageghosts.ps1", "add", "127.0.0.1", projectName + ".local"])

print("Project Name: " + projectName)
print("Magento Version: " + magentoVersion)
print("PHP Version: " + phpVer)
print("Operating system detected as: " + system)

# Copy template directory to new project
copytree('.magento/compose/magento-' + magentoVersion.split(".")[0], "./projects/" + projectName)

call(["mkdir", "-p", "./projects/" + projectName + "/images/nginx"])
call(["mkdir", "-p", "./projects/" + projectName + "/images/php"])
call(["mkdir", "-p", "./projects/" + projectName + "/images/redis"])

copytree('.magento/images/nginx/', "./projects/" + projectName + '/images/nginx/')
copytree('.magento/images/php/' + phpVer, "./projects/" + projectName + '/images/php/')
copytree('.magento/images/redis/', "./projects/" + projectName + '/images/redis/')
# Unpack

if magentoVersion == '2.2':
    call(["tar", "xzf", ".magento/srcfiles/" + magento22, "-C", "./projects/" + projectName + "/src/"])
    binReplace('setup')
    binReplace('cli')
    print("Bin commands updated")
elif magentoVersion == '2.1':
    call(["tar", "xzf", ".magento/srcfiles/" + magento21, "-C", "./projects/" + projectName + "/src/"])
    binReplace('setup')
    binReplace('cli')
    print("Bin commands updated")
elif magentoVersion == '2.0':
    call(["tar", "xzf", ".magento/srcfiles/" + magento20, "-C", "./projects/" + projectName + "/src/"])
    binReplace('setup')
    binReplace('cli')
    print("Bin commands updated")
else:
    call(["tar", "xzf", ".magento/srcfiles/" + magento1, "-C", "./projects/" + projectName + "/"])
    call(["mv", "projects/" + projectName + "/magento/", "projects/" + projectName + "/src/"])
    binReplace('cli')
    print("Bin commands updated")

print("Copy complete")

# Update docker-compose for new project, save the templated adjustments
composeReplace()
print("Compose file updated")

newFile = open('./projects/' + projectName + '/projectdetails', "w+")
newFile.write(projectName)
newFile.close()

# Install Magento2
with cd("./projects/" + projectName):
    call(["docker-compose", "build"])
    call(["docker-compose", "push"])
    call(["docker", "stack", "deploy", "-c", "docker-compose.yml", projectName])

#if magentoVersion != '1':
#    while True:
#        result = run(['./scripts/check_docker_running.sh', projectName], stdout=PIPE)
#        n = result.stdout.decode('utf-8')
#        if "Running" not in n:
#            continue
#        else:
#            with cd("./projects/" + projectName):
#                call(["./bin/setup"])
#                break
