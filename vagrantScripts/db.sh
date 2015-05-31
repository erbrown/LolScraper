#!/bin/bash

########################
# Machine-Specific     #
########################

# Install required software
sudo apt-get install -y mongodb python

# Configure MongoDB to accept external connections
sed -i 's/127.0.0.1/0.0.0.0/g' /etc/mongodb.conf
sudo service mongodb restart
