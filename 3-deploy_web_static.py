#!/usr/bin/python3

"""
Compresses web_static files and send to the web server
"""

from datetime import datetime
from fabric.api import put, run, env, local
from os import path

env.hosts = ['100.26.136.10', '54.236.52.202']


def do_pack():
    """
    Generates a .tgz archive from contents of web_static folder
    """

    now = datetime.now()
    fd = now.strftime("%Y%m%d%H%M%S")
    local("[ -d versions ] || mkdir versions")
    if local(
        f"tar -cvzf versions/web_static_{fd}.tgz web_static"
    ).failed is False:
        return f'versions/web_static_{fd}'
    else:
        return None


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
    if put(archive_path, '/tmp/').failed is True:
        return False

    # Create folder to uncompress archive to
    if run(f'mkdir -p {releases}/{archive_path[9:-4]}/').failed is True:
        return False

    # Uncompress the archive to the folder created above
    if run(
        f'tar -xzf /tmp/{archive_path[9:]} -C {releases}/{archive_path[9:-4]}/'
    ).failed is True:
        return False

    # Move all the files in uncompressed web_static folder to parent folder
    new_release_folder = f'{releases}/{archive_path[9:-4]}'
    web_static_files = f'{new_release_folder}/web_static/*'
    if run(f'mv {web_static_files} {new_release_folder}').failed is True:
        return False

    # Delete the web_static folder (result of uncompressing)
    if run(
        f'rm -rf {releases}/{archive_path[9:-4]}/web_static'
    ).failed is True:
        return False

    # Delete the archive from /tmp
    if run(f'rm /tmp/{archive_path[9:]}').failed is True:
        return False

    # Delete the symbolic link /data/web_static/current
    if run(f'rm {current}').failed is True:
        return False

    # Create new symbolic link, current->
    if run(f'ln -s {releases}/{archive_path[9:-4]} {current}').failed is True:
        return False


def deploy():
    """
    Packs and deploys web_static files
    """

    filename = do_pack()

    if filename is None:
        return False

    return do_deploy(filename)
