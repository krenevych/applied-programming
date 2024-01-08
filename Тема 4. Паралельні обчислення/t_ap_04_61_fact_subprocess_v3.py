# T04/t_ap_04_61_fact_subprocess_v3.py

from subprocess import Popen, PIPE, TimeoutExpired
import logging


logging.basicConfig(level=logging.DEBUG)
logging.debug("starting subprocess")

params = ['python', 't_ap_04_01_fact_thread_v1.py']
ps = Popen(params, stdin=PIPE, stderr=PIPE)

try:
    _, out = ps.communicate(input=b'5', timeout=5)
    print ("out\n", out.decode('utf-8'))
except TimeoutExpired:
    logging.error("Process timeout expired")
