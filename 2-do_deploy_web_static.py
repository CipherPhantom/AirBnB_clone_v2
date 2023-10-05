#!/usr/bin/python3
"""Defines the do_deploy function"""
import os
from fabric.api import put, run, env


env.hosts = ["100.26.18.88", "54.197.46.69"]


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
