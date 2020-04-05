import logging
import gevent
from gevent import pywsgi
from server import Server


class WebServer(Server):
    def __init__(self, port, web_main_function):
        self._port = port
        self._serving = False
        self._serving_greenlet = None
        self._web_server = None
        self._logger = logging.getLogger(__name__)
        self._web_main_function = web_main_function

    def __serve(self):
        self._logger.info("[WebServer] initialized on port " + str(self._port) + " ...")
        self._web_server = pywsgi.WSGIServer(('', self._port), self._web_main_function)
        self._web_server.serve_forever()

    def start_server(self):
        if not self._serving:
            self._serving_greenlet = gevent.spawn(self.__serve)
            self._serving = True
            gevent.sleep(0)

    def stop_server(self):
        if self._serving:
            gevent.kill(self._serving_greenlet)
            self._serving = False
            self._web_server.close()
            self._logger.info("[WebServer] shut down")



