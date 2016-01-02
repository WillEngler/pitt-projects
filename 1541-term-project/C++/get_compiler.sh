#!/usr/bin/env bash
#The above line specifies what shell this
# script needs to run on.

#Go to the folder shared by the host and guest OS's.
cd /vagrant


apt-get update
apt-get install -y g++