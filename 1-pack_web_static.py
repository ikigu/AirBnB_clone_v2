#!/usr/bin/python3

"""
Compresses web_static files
"""

from datetime import datetime
from fabric.api import local


def do_pack():
    """
    Generates a .tgz archive from contents of web_static folder
    """

    now = datetime.now()
    fd = now.strftime("%Y%m%d%H%M%S")
    local("[ -d versions ] || mkdir versions")
    local(f"tar -cvzf versions/web_static_{fd}.tgz web_static")
