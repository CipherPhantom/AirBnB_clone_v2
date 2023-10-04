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

    cmd = put(archive_path, "/tmp/")
    cmd_1 = run("mkdir -p {}".format(release_dir))
    cmd_2 = run("tar -xzf /tmp/{} -C {}".format(archive_file, release_dir))
    cmd_3 = run("rm /tmp/{}".format(archive_file))
    cmd_4 = run("mv {}web_static/* {}".format(release_dir, release_dir))
    cmd_5 = run("rm -rf {}web_static".format(release_dir))
    cmd_6 = run("rm -rf /data/web_static/current")
    cmd_7 = run("ln -s {} /data/web_static/current".format(release_dir))

    if cmd.failed or cmd_1.failed or cmd_2.failed or cmd_3.failed or \
            cmd_4.failed or cmd_5.failed or cmd_6.failed or cmd_7.failed:
        return False
    return True
