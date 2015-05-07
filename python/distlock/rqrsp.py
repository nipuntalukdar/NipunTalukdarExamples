!#/usr/bin/env python

from Queue import Queue, Full, Empty
import logging

class RequestResponse:

    def __init__(self, ownerid):
        self.rqs = Queue(20480)
        self.rsps = Queue(20480)
        self.owner = ownerid

    def add_request(self, request):
        try:
            self.rqs.put(request, True, 10)
            return True
        except Full as fulex:
            logging.error(fulex)
            return False

    def take_request(self):
        if self.rqs.empty():
            return None
        try:
            return self.rqs.get(True, 1)
        except Empty as empe:
            logging.error(empe)
            return None

    def add_response(self, response):
        try:
            self.rsps.put(response, True, 10)
            return True
        except Full as fulex:
            logging.error(fulex)
            return False

    def take_response(self):
        if self.rsps.empty():
            return None
        try:
            return self.rsps.get(True, 1)
        except Empty as empe:
            logging.error(empe)
            return None
