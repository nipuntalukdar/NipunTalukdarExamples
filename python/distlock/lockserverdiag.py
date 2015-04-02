#!/usr/bin/python

import time
import threading
import logging

class LockSeverDiag(threading.Thread):

    def __init__(self, lc):
        threading.Thread.__init__(self)
        self.lc = lc
        self.keep_running = True

    def stop(self):
        self.keep_running = False

    def run(self):
        while self.keep_running:
            self.lc.print_diagnostics()
            time.sleep(60)
