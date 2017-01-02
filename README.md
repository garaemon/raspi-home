# [raspi-home](https://github.com/garaemon/raspi-home.git) [![Build Status](https://travis-ci.org/garaemon/raspi-home.svg?branch=master)](https://travis-ci.org/garaemon/raspi-home)
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

## setup cron

Edit cron like below:
```
$ crontab -l
@reboot /home/pi/deploy-raspi-home/run.sh 2>&1 | tee /tmp/raspi.log
*/5 * * * * /home/pi/deploy-raspi-home/restart.sh 2>&1
```
