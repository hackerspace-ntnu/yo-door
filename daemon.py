#!/usr/bin/env python
# -*- coding: utf-8 -*-

from daemonize import Daemonize

from yo import main


APP_NAME = "yo-door"
PID = "/tmp/{}.PID".format(APP_NAME)

if __name__ == "__main__":
    daemon = Daemonize(app=APP_NAME, pid=PID, action=main)
    daemon.start()