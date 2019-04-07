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

# git 
sudo apt-get install git-core
sudo git clone https://github.com/kimikadze/web-rcat.git

----------------------------------------------

#treetagger
- load files from page
- install via sh
- define path variables:
	- export PATH=/rcat/treetagger_installation/cmd:$PATH
	- export PATH=/rcat/treetagger_installation/bin:$PATH

	- export PATH=/home/barthfn/treetagger_installation_2/cmd:$PATH
	- export PATH=/home/barthfn/treetagger_installation_2/bin:$PATH

#WSGI Entry Point
uwsgi --socket 185.248.140.172:5000 --protocol=http -w wsgi:app

# python packages (not in environment)

## as user barthfn
pip3 install --upgrade pip

pip3 install nltk
pip3 install wheel
sudo pip3 install matplotlib
sudo apt-get install python3-tk
(=tkinter)
sudo pip3 install pylatex
sudo pip3 install wordcloud
sudo -H pip install treetaggerwrapper

## in environment rcatenv from barthfn
sudo -H pip install wheel
sudo -H pip install uwsgi flask

##as user root (since barthfn had permission errors also with sudo)
pip3 install --upgrade pip

### RUN PAGE
python3 flask_form.py 

Runs so far at:
http://185.248.140.172:5000

But file upload doesn't work.








