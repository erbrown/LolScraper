#!/bin/bash

########################
# Boiler Plate Install #
########################

# Update the boxes
sudo apt-get update
sudo apt-get -y dist-upgrade

# Install utility software
sudo apt-get install -y screen vim
