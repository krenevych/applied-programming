# T04/t_ap_04_61_fact_subprocess_v1.py

from subprocess import run
import logging

logging.basicConfig(level=logging.DEBUG)

logging.debug("starting subprocess")

params = ['python', 't_ap_04_01_fact_thread_v1.py']
run(params)
