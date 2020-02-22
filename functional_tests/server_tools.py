#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fabric import Config, Connection


def _get_manage_dot_py(host):
    return f'~/sites/{host}/virtualenv/bin/python ~/sites/{host}/manage.py'


def _get_hostname(ssh_config_path):
    with open(ssh_config_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith('Host '):
                return line.replace('Host ', '')
        return None


def reset_database(ssh_config_path):
    config = Config(
        runtime_ssh_path=ssh_config_path
    )
    host = _get_hostname(ssh_config_path)
    with Connection(host=host, config=config) as c:
        manage_dot_py = _get_manage_dot_py(c.host)
        c.run(f'{manage_dot_py} flush --noinput')


def _get_server_env_vars(c, host):
    env_lines = c.run(
        f'cat ~/sites/{host}/.env',
        hide=True).stdout.strip().splitlines()
    return dict(l.split('=') for l in env_lines if l)


def create_session_on_server(ssh_config_path, email):
    config = Config(
        runtime_ssh_path=ssh_config_path
    )
    host = _get_hostname(ssh_config_path)
    with Connection(host=host, config=config) as c:
        manage_dot_py = _get_manage_dot_py(c.host)
        env_vars = _get_server_env_vars(c, c.host)
        c.config.run.env = env_vars
        session_key = c.run(
            f'{manage_dot_py} create_session {email}',
            hide=True).stdout.strip()
        return session_key
