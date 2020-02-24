Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3.6
* virtualenv + pip
* Git

eg, on Ubuntu:
    sudo apt update
    sudo apt upgrade -y
    sudo apt install nginx python3-venv

## Nginx Virtual Host config

```
# start nginx
sudo systemctl start nginx

# create a nginx config
export SITENAME=www.example.com
sudo vim /etc/nginx/sites-available/$SITENAME

* see nginx.template.conf
* replace DOMAIN with, e.g., www.example.com

# create a symlink to the config in sites-enabled
cd /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/$SITENAME $SITENAME
readlink -f $SITENAME

# remove the default nginx config in sites-enabled
sudo rm /etc/nginx/sites-enabled/default

# reload nginx
sudo systemctl reload nginx
```

## Systemd service

```
# create a systemd service
sudo vim /etc/systemd/system/gunicorn-www.example.com.service

* see gunicorn-systemd.template.service
* replace DOMAIN with, e.g., www.example.com

# tell systemd to load our new config
sudo systemctl daemon-reload

# tell systemd to always load our new config on boot
sudo systemctl enable gunicorn-www.capybara-mt.com.service

# tell systemd to start our service
sudo systemctl start gunicorn-www.capybara-mt.com.service
```

## Folder structure

Assume we have a user account at /home/username

/home/username
└── sites
    ├── DOMAIN1
    │   ├-- .env
    │   ├-- db.sqlite3
    │   ├-- manage.py etc
    │   ├-- static
    │   └── virtualenv
    └── DOMAIN2
        ├-- .env
        ├-- db.sqlite3
        └── etc


## Provisioning a CI server

```
# install java11
sudo apt install openjdk-11-jdk

# install jenkins
wget --no-check-certificate -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > \
    /etc/apt/sources.list.d/jenkins.list'
sudo apt-get update
sudo apt-get install jenkins


sudo apt install python3-venv
sudo apt install firefox xvfb
sudo apt install build-essential libssl-dev libffi-dev

wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
tar -xvzf geckodriver-v0.26.0-linux64.tar.gz
sudo mv geckodriver /usr/local/bin
geckodriver --version
geckodriver 0.26.0 (e9783a644016 2019-10-10 13:38 +0000)

```