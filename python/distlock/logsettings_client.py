#!/usr/bin/env python

from threading import Lock
import logging

cli_log_inited = False
lck = Lock()
def init_logging(logfile='/tmp/lockclient.log'):
    global cli_log_inited
    if not cli_log_inited:
        lck.acquire()
        if not cli_log_inited:
            FORMAT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d  %(message)s'
            logging.basicConfig(filename = logfile, format = FORMAT, \
                    level = logging.DEBUG)
            logging.debug("Logging initied")
            cli_log_inited = True
        lck.release()
