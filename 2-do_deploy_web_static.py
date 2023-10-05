#!/usr/bin/python3
"""Defines the do_deploy function"""
import os
from fabric.api import put
from fabric.api import run
from fabric.api import env


env.hosts = ["100.26.18.88", "54.197.46.69"]


def do_deploy(archive_path):
    """Distributes an archive to web servers"""
    if not os.path.isfile(archive_path):
        return False

    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/").failed:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
            file, name)).failed:
        return False
    if run("rm -f /tmp/{}".format(file)).failed:
        return False
    web_static = "/data/web_static/releases/{}/web_static/*".format(name)
    cmd = "mv {} /data/web_static/releases/{}/".format(web_static, name)
    if run(cmd).failed:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".format(
            name)).failed:
        return False
    if run("rm -rf /data/web_static/current").failed:
        return False
    cmd = "ln -s /data/web_static/releases/{}/ /data/web_static/current"
    if run(cmd.format(name)).failed:
        return False
    return True
