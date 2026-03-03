#! /usr/bin/env python3


from repo_helper.Repo_Helper import Repo_Helper

helper = Repo_Helper()
helper.execute(command=f"socat PTY,link=/home/developer/workspace/tty1,raw,echo=0 tcp:dw-latitude-e6440:3002", wait=False)
