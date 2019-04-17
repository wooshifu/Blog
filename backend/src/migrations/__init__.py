"""
this directory is used for upgrade database schemas, if you changed the database DDL,
you should add a file named 'mxxxxxxxx.py' to define the upgrading process.
"""

import re
from pathlib import Path
from models.migration import Migration as MigrationModel

from .migration import Migration

__current_dir = Path(__file__).parent
__files = [f.stem for f in __current_dir.iterdir()]

_migration_file_pattern = re.compile(r'm\d{8}')
_migrations = sorted(filter(lambda file_name: re.match(_migration_file_pattern, file_name), __files))

_latest_migration = MigrationModel.query.order_by(MigrationModel.id.desc()).first()

if _latest_migration is None:
    for migration in _migrations:
        exec(f'from . import {migration}')
        exec(f'{migration}.{migration.upper()}.{Migration.run_upgrade.__name__}("{migration}")')
else:
    for migration in _migrations:
        if migration > _latest_migration.migration:
            exec(f'from . import {migration}')
            exec(f'{migration}.{migration.upper()}.{Migration.run_upgrade.__name__}("{migration}")')
