import abc

import sqlalchemy
from sqlalchemy import event

from alembic.operations import Operations
from alembic.runtime.migration import MigrationContext
from app.db import db_connection, db_engine
from app import db

from models.migration import Migration as MigrationModel


class Migration(abc.ABCMeta):
    __description__: str = ''

    @classmethod
    def run_upgrade(mcs, current_version, silent=False):

        ctx = MigrationContext.configure(db_connection)
        op = Operations(ctx)
        try:
            print(f'running upgrade {current_version}')
            event.listen(db_engine, 'before_cursor_execute', _before_cursor_execute)
            mcs.upgrade(op, sqlalchemy, silent=silent)
            event.remove(db_engine, 'before_cursor_execute', _before_cursor_execute)
            sql, param = _MigrationEvent.get_last_record()
            migration = MigrationModel(migration=current_version,
                                       sql=sql,
                                       parameter=param,
                                       description=str(mcs.__description__))
            db.session.add(migration)
            db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError as exc:  # noqa
            print(f'error occurred: {exc}')
            if not silent:
                raise exc

    @classmethod
    @abc.abstractmethod
    def upgrade(mcs, op: Operations, sa: sqlalchemy, silent: bool) -> None:
        """
        do the upgrade process

        :param op: operations alembic provided
        :param sa: sqlalchemy module
        :param silent: if True, error will be thrown when error occurred
        """
        raise NotImplementedError


def _before_cursor_execute(conn, cursor, statement, parameters, context, executemany):  # noqa
    _MigrationEvent.last_sql.append(str(statement))
    _MigrationEvent.last_sql_param.append(str(parameters) if parameters else '')


class _MigrationEvent:
    last_sql, last_sql_param = [], []

    @classmethod
    def get_last_record(cls):
        split = '\n-----\n'
        sql, param = split.join(cls.last_sql), split.join(cls.last_sql_param)
        cls.last_sql, cls.last_sql_param = [], []
        return sql, param
