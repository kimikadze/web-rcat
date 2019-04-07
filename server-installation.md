# host-unlimited-server

# links
https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-18-04

https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04#step-3-%E2%80%94-setting-up-a-flask-application


# users+passwords
ssh root@185.248.140.172
b61u3bas

ssh barthfn@185.248.140.172
123456

ssh kimey@185.248.140.172
123456

------------------------------------------------

# update + pip3
sudo apt update

sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools

# nano
sudo apt-get install nano

#configure locales
apt-get install locales
locale-gen en_US.UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export LANGUAGE=en_US.UTF-8

sudo nano /etc/default/locale

----------------------------------------------

# environment for flask app

sudo apt install python3-venv

cd /
sudo mkdir rcat
cd rcat/
sudo python3 -m venv rcatenv
source rcatenv/bin/activate

----------------------------------------------

# python packages in environment

sudo -H pip install wheel
sudo -H pip install uwsgi flask

#




# python packages (not in environment)

## as user barthfn
pip3 install --upgrade pip
pip3 install nltk


##as user root (since barthfn had permission errors also with sudo)
pip3 install --upgrade pip
pip3 install treetaggerwrapper



