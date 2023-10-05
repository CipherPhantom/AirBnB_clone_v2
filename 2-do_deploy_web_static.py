#!/usr/bin/python3
"""Defines the do_deploy function"""
import os
import datetime
from fabric.api import put, run, env, local


env.hosts = ["100.26.18.88", "54.197.46.69"]


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    if not os.path.exists("versions"):
        os.makedirs("versions")
    date = datetime.datetime.now()
    tgz_file_path = "versions/web_static_{}{}{}{}{}{}.tgz".format(
            date.year,
            date.month,
            date.day,
            date.hour,
            date.minute,
            date.second
            )
    result = local("tar -cvzf {} web_static".format(tgz_file_path))
    if result.failed:
        return None
    return tgz_file_path


def do_deploy(archive_path):
    """Distributes an archive to  web servers"""
    if not os.path.exists(archive_path):
        return False

    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/").failed:
        return False
    if run(f"mkdir -p /data/web_static/releases/{name}/").failed:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
            file, name)).failed:
        return False
    if run(f"rm -f /tmp/{file}").failed:
        return False
    web_static = f"/data/web_static/releases/{name}/web_static/*"
    cmd = f"mv {web_static} /data/web_static/releases/{name}/"
    if run(cmd).failed:
        return False
    if run(f"rm -rf /data/web_static/releases/{name}/web_static").failed:
        return False
    if run(f"rm -rf /data/web_static/current").failed:
        return False
    cmd = f"ln -s /data/web_static/releases/{name}/ /data/web_static/current"
    if run(cmd).failed:
        return False
    return True
