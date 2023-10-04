#!/usr/bin/python3
"""Defines a do_deploy function"""
import os
from fabric.api import env, put, run


env.hosts = ["54.197.46.69", "100.26.18.88"]
env.user = "ubuntu"


def do_deploy(archive_path):
    """Distributes an archive to your web servers."""
    if not os.path.exists(archive_path):
        return False

    archive_file = archive_path.split("/")[-1]
    archive_dir = archive_file.split(".")[0]

    release_dir = "/data/web_static/releases/{}/".format(archive_dir)

    put(archive_path, "/tmp/")
    run("mkdir -p {}".format(release_dir))
    run("tar -xzf /tmp/{} -C {}".format(archive_file, release_dir))
    run("rm /tmp/{}".format(archive_file))
    run("mv {}web_static/* {}".format(release_dir, release_dir))
    run("rm -rf {}web_static".format(release_dir))
    run("rm -rf /data/web_static/current")
    run("ln -s {} /data/web_static/current".format(release_dir))

    return True
