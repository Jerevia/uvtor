from uvtor.conf import settings
from playhouse import postgres_ext
from playhouse import pool
import peewee_async


database = peewee_async.PooledPostgresqlDatabase(
    settings.DB_DATABASE, user=settings.DB_USER,
    host=settings.DB_HOST,
    password=settings.DB_PASSWORD,
    min_connections=settings.DB_CONN_POOL_MIN_SIZE,
    max_connections=settings.DB_CONN_POOL_MAX_SIZE)

pg_db = pool.PooledPostgresqlExtDatabase(
    settings.DB_DATABASE, user=settings.DB_USER,
    host=settings.DB_HOST,
    password=settings.DB_PASSWORD,
    min_connections=settings.DB_CONN_POOL_MIN_SIZE,
    max_connections=settings.DB_CONN_POOL_MAX_SIZE
    )

manager = peewee_async.Manager(database)


class BaseModel(postgres_ext.Model):

    class Meta:
        database = database
