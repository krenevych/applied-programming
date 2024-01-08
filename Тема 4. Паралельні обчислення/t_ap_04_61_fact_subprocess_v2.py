# T04/t_ap_04_61_fact_subprocess_v2.py

from subprocess import run
import logging
import sys

logging.basicConfig(level=logging.DEBUG)
logging.debug("starting subprocess")

params = ['python', 't_ap_04_01_fact_thread_v1.py']
completed = run(params, stdin=sys.stdin, stderr=sys.stdout)
if completed.returncode != 0:
    logging.error("subprocess terminated with error %s", completed.returncode)

