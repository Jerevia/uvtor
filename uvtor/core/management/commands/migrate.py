from uvtor.core.management.base import BaseCommand, CommandError
from uvtor.db.migrations import Router
from uvtor.conf import settings
from playhouse.pool import PooledPostgresqlExtDatabase
import os


class Command(BaseCommand):
    def check(self):
        if not os.path.exists('.uvtor'):
            raise CommandError('Invalid uvtor project')

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('-e', '--env', type=str,
                            help='Env.', default='TEST')

    def execute(self, *args, **options):
        self.check()
        _env = options.get('env')
        conf = getattr(settings, 'ENVS')[_env]

        db = PooledPostgresqlExtDatabase(
            conf.get('database'), user=conf.get('user'),
            host=conf.get('host'),
            password=conf.get('password'),
            register_hstore=False)
        db.connect()
        router = Router(db)
        router.run()
        db.close()
