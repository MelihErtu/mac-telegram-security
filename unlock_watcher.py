#!/usr/bin/env python3
import subprocess, time
from pathlib import Path
MAIN = Path(__file__).resolve().parent / 'imac_security.py'

def locked():
    try:
        out=subprocess.check_output(['/usr/sbin/ioreg','-n','Root','-d1','-a'], text=True)
        return 'CGSSessionScreenIsLocked' in out
    except Exception: return False

prev=locked(); last_trigger=0; child=None
while True:
    cur=locked()
    if prev and not cur and time.time()-last_trigger>10:
        if child is None or child.poll() is not None:
            child=subprocess.Popen(['/usr/bin/python3', str(MAIN)])
            last_trigger=time.time()
    prev=cur
    time.sleep(1)
