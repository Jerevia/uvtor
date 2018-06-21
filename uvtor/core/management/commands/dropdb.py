from uvtor.core.management.base import BaseCommand, CommandError
from uvtor.conf import settings
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2
import os


class Command(BaseCommand):

    def check(self):
        if not os.path.exists('.uvtor'):
            raise CommandError('Invalid uvtor project')

    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument('-e', '--env', type=str,
                            help='Env.', default='TEST')
        parser.add_argument(
            '--defaultdb', '-d',
            help='Default db connection session.',
            metavar=('DB_NAME'))

    def _get_conn(self, default_db, env='TEST'):
        conf = getattr(settings, 'ENVS')[env]
        con = psycopg2.connect(database=default_db, user=conf.get(
            'user'), host=conf.get('host'), password=conf.get('password'))
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return con

    def _drop_db(self, env, name, default_db):
        conf = getattr(settings, 'ENVS')[env]
        _name = conf.get('database')
        con = self._get_conn(default_db, env)
        cur = con.cursor()
        cur.execute(f'DROP DATABASE {_name} ;')

        print(f'Drop database {_name} successfully')

    def execute(self, **options):
        _env = options.get('env')
        _name = options.get('name')
        _db = options.get('defaultdb')

        print('Using env %s' % _env)
        self._drop_db(_env, _name, _db)
