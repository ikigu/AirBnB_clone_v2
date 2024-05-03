#!/usr/bin/env bash
pip3 uninstall Fabric
sudo apt-get install libffi-dev
sudo apt-get install libssl-dev
sudo apt-get install build-essential
sudo apt-get install python3.4-dev
sudo apt-get install libpython3-dev
pip install pyparsing
pip install appdirs
pip install setuptools==40.1.0
pip install cryptography==2.8
pip install bcrypt==3.1.7
pip install PyNaCl==1.3.0
pip install Fabric3==1.14.post1