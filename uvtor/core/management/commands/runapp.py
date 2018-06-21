from tornado.platform.asyncio import AsyncIOMainLoop
from tornado.log import enable_pretty_logging
from tornado.options import options as _ops
from uvtor.core.management.base import BaseCommand, CommandError
from uvtor.core import make_app
import asyncio
import uvloop
import os
import logging


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

AsyncIOMainLoop().install()


class Command(BaseCommand):

    def check(self):
        if not os.path.exists('.uvtor'):
            raise CommandError('Invalid uvtor project')

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            'name', metavar='name',
            help='Name of app',
        )
        parser.add_argument(
            '--port', '-P', metavar='port',
            default=8000,
            help='Listen port',
        )

        parser.add_argument(
            '--logging', '-L', metavar='port',
            default='INFO',
            help='Logging Level',
        )

        parser.add_argument(
            '--address', '-H', metavar='address',
            default='127.0.0.1',
            help='Listen address',
        )
        parser.add_argument(
            '--autoreload',
            help='Enable autoreload',
            action='store_true'
        )

    def execute(self, **options):
        _appname = options.get('name')
        _address = options.get('address')
        _port = options.get('port')
        _autoreload = options.get('autoreload')
        _logging = options.get('logging')
        _app = make_app(_appname, _autoreload)
        _app.listen(_port, address=_address)
        _ops.logging = _logging
        enable_pretty_logging(_ops)
        logging.info(f'Server started, listen on {_address}:{_port}')
        try:
            asyncio.get_event_loop().run_forever()
        except KeyboardInterrupt as e:
            asyncio.get_event_loop().close()
