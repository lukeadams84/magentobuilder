#!/usr/bin/env bash

[ -z "$1" ] && echo "Please specify a project name" && exit

# Get ID of current project phpfpm container

projectName="$1";

result="$(docker stack ps -f name=$1_phpfpm --format {{.CurrentState}} $1)";
echo $result;
