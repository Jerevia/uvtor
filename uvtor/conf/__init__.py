from aiocache import caches
import tornado.httpclient
import os
import sys


class Settings(object):

    def __init__(self):
        sys.path.insert(0, os.getcwd())
        settings = __import__('settings')
        for _ in dir(settings):
            if not (_.startswith('__') and _.endswith('__')):
                setattr(self, _, getattr(settings, _))
        self._set_http_max_client()
        self._set_cache()

    def _set_http_max_client(self):
        if not hasattr(self, 'HTTP_MAX_CLIENT'):
            setattr(self, 'HTTP_MAX_CLIENT', 1000)
        tornado.httpclient.AsyncHTTPClient.configure(
            None, max_clients=int(self.HTTP_MAX_CLIENT))

    def _set_cache(self):
        if not hasattr(self, 'CACHES'):
            return
        caches.set_config(self.CACHES)


try:
    settings = Settings()
except ModuleNotFoundError:
    settings = None


__ALL__ = [
    settings
]
