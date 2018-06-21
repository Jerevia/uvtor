from uvtor.core.management.base import BaseCommand
from uvtor.conf import settings
import os
import datetime


class Command(BaseCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--env', '-e', type=str,
                            help='Env.', default='TEST')

    def _init_file(self, filename):
        with open(filename, 'w') as file:
            file.write("""expressions = [

    ]
    """)

    def _create_migration_file(self):
        directory = os.path.join(settings.ROOT_DIR, 'models', 'migrations')

        _index = max([int(_file.split('_')[0]) for _file in os.listdir(
            directory) if _file.split('_')[0].isdigit()]) + 1
        _file = os.path.join(directory, '%04d_auto_%s.py' % (
            _index, datetime.datetime.strftime(
                datetime.datetime.now(), '%Y%m%d_%H%M')))
        os.mknod(_file)
        self._init_file(_file)
        return True

    def execute(self, **options):
        _env = options.get('env')
        print('Using env %s' % _env)
        self._create_migration_file()
        print('New migration file is successfully created')
