"""
    The package description.

"""
import datetime
import logging

import peewee as pw

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.StreamHandler())
LOGGER.setLevel(logging.INFO)


class MigrateHistory(pw.Model):

    """Presents the migrations in database."""

    name = pw.CharField()
    migrated_at = pw.DateTimeField(default=datetime.datetime.utcnow)

    def __unicode__(self):
        """String representation."""
        return self.name


from .router import Migrator, Router  # noqa
