#!/usr/bin/python3

"""
Compresses web_static files and send to the web server
"""

from datetime import datetime
from fabric.api import local, put, run, sudo
from fabric.state import env
from os import path

env.hosts = ['100.26.136.10', '54.236.52.202']


def do_pack():
    """
    Generates a .tgz archive from contents of web_static folder
    """

    now = datetime.now()
    fd = now.strftime("%Y%m%d%H%M%S")
    local("[ -d versions ] || mkdir versions")
    local(f"tar -cvzf versions/web_static_{fd}.tgz web_static")


def do_deploy(archive_path):
    """
    Deploys the archive to the server

    Args:
        archive_path (str): the location of the web_static files
    """

    if not path.exists(archive_path):
        return False

    current = '/data/web_static/current'
    releases = '/data/web_static/releases'

    # Upload the archive to the /tmp/ directory of the web server
    if put(archive_path, '/tmp/').failed:
        return False

    # Create folder to uncompress archive to
    if sudo(f'mkdir -p {releases}/{archive_path[9:-4]}/').failed:
        return False

    # Uncompress the archive to the folder created above
    if sudo(
        f'tar -xzf /tmp/{archive_path[9:]} -C {releases}/{archive_path[9:-4]}/'
    ).failed:
        return False

    # Delete the archive from /tmp
    if sudo(f'rm /tmp/{archive_path[9:]}').failed:
        return False

    # Delete the symbolic link /data/web_static/current
    if sudo(f'rm {current}').failed:
        return False

    # Create new symbolic link, current->
    if sudo(f'ln -s {releases}/{archive_path[:-4]} {current}').failed:
        return False
