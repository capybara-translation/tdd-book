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
