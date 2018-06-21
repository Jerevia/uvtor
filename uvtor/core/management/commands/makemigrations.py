from uvtor.core.management.base import BaseCommand, CommandError
from uvtor.db.migrations import Router
from uvtor.conf import settings
from uvtor.db.models import BaseModel
from playhouse.pool import PooledPostgresqlExtDatabase
import pkgutil
import os
import inspect

CURDIR = os.getcwd()
DEFAULT_MODEL_DIR = os.path.join(CURDIR, 'models')


class Command(BaseCommand):
    def check(self):
        if not os.path.exists('.uvtor'):
            raise CommandError('Invalid uvtor project')

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('-e', '--env', type=str,
                            help='Env.', default='TEST')
        parser.add_argument(
            '-m',
            '--model',
            type=str,
            help='Set path to your models module.',
            default=None)

    def execute(self, *args, **options):
        self.check()
        _env = options.get('env')
        _model = options.get('model')
        conf = getattr(settings, 'ENVS')[_env]
        db = PooledPostgresqlExtDatabase(
            conf.get('database'), user=conf.get('user'),
            host=conf.get('host'),
            password=conf.get('password'),
            register_hstore=False)
        db.connect()
        router = Router(db)
        if not _model:
            _models = pkgutil.importlib.import_module('models')
            for loader, modname, ispkg in pkgutil.iter_modules(
                    _models.__path__, prefix='models.'):
                _m = pkgutil.importlib.import_module(modname)
                for _, _ins in _m.__dict__.items():

                    if inspect.isclass(_ins) and issubclass(
                            _ins, BaseModel) and _ins != BaseModel:
                        setattr(
                            _models,
                            _ins.__module__ + '.' + _ins.__name__,
                            _ins)
            if hasattr(_models, 'models.BaseModel'):
                delattr(_models, 'models.BaseModel')
            router.create(auto=_models)
        else:
            _model = f'models.{_model}'
            router.create(auto=_model)
        db.close()
