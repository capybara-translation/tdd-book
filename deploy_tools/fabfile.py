#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import random
import json
from invoke import task, run
from patchwork.files import append, exists
from fabric import Config, Connection

REPO_URL = 'https://github.com/capybara-translation/tdd-book.git'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SSH_CONFIG = None
APP_CONFIG = None


def load_ssh_config(ssh_config_file):
    ssh_config_file = os.path.basename(ssh_config_file)
    ssh_config_path = os.path.join(BASE_DIR, ssh_config_file)
    return Config(
        runtime_ssh_path=ssh_config_path
    )


def load_app_config(app_config_file):
    app_config_file = os.path.basename(app_config_file)
    app_config_path = os.path.join(BASE_DIR, app_config_file)
    with open(app_config_path) as f:
        return json.load(f)


@task
def staging(c, ssh_config_file, app_config_file):
    global SSH_CONFIG
    global APP_CONFIG
    # Load ssh config
    SSH_CONFIG = load_ssh_config(ssh_config_file)

    # Load app config
    APP_CONFIG = load_app_config(app_config_file)

    c.name = 'staging'


@task
def production(c, ssh_config_file, app_config_file):
    global SSH_CONFIG
    global APP_CONFIG
    # Load ssh config
    SSH_CONFIG = load_ssh_config(ssh_config_file)

    # Load app config
    APP_CONFIG = load_app_config(app_config_file)

    c.name = 'production'


@task
def deploy(c):
    with Connection(host=c.name, config=SSH_CONFIG) as c:
        site_folder = f'/home/{c.user}/sites/{c.host}'
        c.run(f'mkdir -p {site_folder}')
        with c.cd(site_folder):
            _get_latest_source(c)
            _update_virtual_env(c)
            _create_or_update_dotenv(c)
            _update_static_files(c)
            _update_database(c)


def _get_latest_source(c):
    print('Getting latest source...')
    if exists(c, '.git'):
        c.run('git fetch')
    else:
        c.run(f'git clone {REPO_URL} .')
    current_commit = run("git log -n 1 --format=%H", hide=True).stdout.strip()
    c.run(f'git reset --hard {current_commit}')
    print('Done\n')


def _update_virtual_env(c):
    print('Updating virtualenv...')
    if not exists(c, 'virtualenv/bin/pip'):
        c.run(f'python3 -m venv virtualenv')
    c.run('./virtualenv/bin/pip install -r requirements.txt')
    print('Done\n')


def _create_or_update_dotenv(c):
    print('Creating/Updating dotenv...')
    append(c, '.env', 'DJANGO_DEBUG_FALSE=y')
    append(c, '.env', f'SITENAME={c.host}')
    append(c, '.env', f'EMAIL_USER=${APP_CONFIG["EMAIL_USER"]}')
    append(c, '.env', f'EMAIL_PASSWORD=${APP_CONFIG["EMAIL_PASSWORD"]}')
    current_contents = c.run('cat .env', hide=True).stdout.strip()
    if 'DJANGO_SECRET_KEY' not in current_contents:
        new_secret = ''.join(random.SystemRandom().choices(
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50))
        append(c, '.env', f'DJANGO_SECRET_KEY={new_secret}')
    print('Done\n')


def _update_static_files(c):
    print('Updating static files...')
    c.run('./virtualenv/bin/python manage.py collectstatic --noinput')
    print('Done\n')


def _update_database(c):
    print('Updating database...')
    c.run('./virtualenv/bin/python manage.py migrate --noinput')
    print('Done\n')
