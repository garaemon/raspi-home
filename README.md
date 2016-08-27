# raspi-home [![Build Status](https://travis-ci.org/garaemon/raspi-home.svg?branch=master)](https://travis-ci.org/garaemon/raspi-home)
# setup host machine

## Install ansible on host machine
### mac os x
```
brew install ansible
```

# setup rasberry pi
```
ansible-playbook -i ipaddress, raspi3.yaml --ask-pass
```
