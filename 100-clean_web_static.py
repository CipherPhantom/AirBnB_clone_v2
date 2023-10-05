#!/usr/bin/python3
"""Define a do_clean function"""
import os
from fabric.api import run
from fabric.api import local
from fabric.api import env
from fabric.api import lcd
from fabric.api import cd

env.hosts = ["100.26.18.88", "54.197.46.69"]


def do_clean(number=0):
    """deletes out-of-date archives"""

    number = 1 if int(number) == 0 else int(number)
    if os.path.exists("versions") and os.path.isdir("versions"):
        archives = sorted(os.listdir("versions"))
        with lcd("versions"):
            for file in archives[:-number]:
                local("rm ./{}".format(file))

    with cd("/data/web_static/releases"):
        releases = run("ls -tr").split()
        releases = [ver for ver in releases if "web_static_" in ver]
        for version in releases[:-number]:
            run("rm -rf ./{}".format(version))
