#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fabric import Config, Connection


def _get_manage_dot_py(host):
    return f'~/sites/{host}/virtualenv/bin/python ~/sites/{host}/manage.py'


def reset_database(ssh_config_path):
    config = Config(
        runtime_ssh_path=ssh_config_path
    )
    manage_dot_py = _get_manage_dot_py(config.host)
    with Connection(host=config.name, config=config) as c:
        c.run(f'{manage_dot_py} flush --noinput')


def _get_server_env_vars(c, host):
    env_lines = c.run(f'cat ~/sites/{host}/.env').splitlines()
    return dict(l.split('=') for l in env_lines if l)


def create_session_on_server(ssh_config_path, email):
    config = Config(
        runtime_ssh_path=ssh_config_path
    )
    manage_dot_py = _get_manage_dot_py(config.host)
    with Connection(host=config.name, config=config) as c:
        env_vars = _get_server_env_vars(c, config.host)
        c.config.run.env = env_vars
        session_key = c.run(
            f'{manage_dot_py} create_session {email}',
            hide=True).stdout.strip()
        print(session_key)
        return session_key
