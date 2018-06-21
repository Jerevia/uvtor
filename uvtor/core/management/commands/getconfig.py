from uvtor.core.management.base import BaseCommand
from uvtor.utils import config
import os
import sys
import getpass


class Command(BaseCommand):

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            'name', metavar='name',
            help='Name of software',
        )
        parser.add_argument(
            '--domain', '-D', metavar='domain',
            help='Domain',
        )
        parser.add_argument(
            '--listen', '-P', metavar='listen',
            default=80,
            help='listening port',
        )
        parser.add_argument(
            '--log_dir', '-L', metavar='log_dir',
            help='Log directory',
        )
        parser.add_argument(
            '--user', '-U', metavar='user',
            default=getpass.getuser(),
            help='User',
        )

    def execute(self, **options):
        sys.path.insert(0, os.getcwd())
        _name = options.get('name')
        if _name == 'nginx':
            print(config.create_nginx_config(
                options.get('domain'),
                options.get('listen'),
                options.get('log_dir')
                ))
        elif _name == 'supervisor':
            print(config.create_supervisor_config(
                options.get('log_dir'),
                options.get('user'),
                ))
