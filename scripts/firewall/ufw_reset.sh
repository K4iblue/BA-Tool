#!/bin/bash

# Reset UFW
sudo ufw --force reset

# Remove all old rule files
sudo rm -r /etc/ufw/after.rules.*
sudo rm -r /etc/ufw/after6.rules.*
sudo rm -r /etc/ufw/before.rules.*
sudo rm -r /etc/ufw/before6.rules.*
sudo rm -r /etc/ufw/user.rules.*
sudo rm -r /etc/ufw/user6.rules.*
