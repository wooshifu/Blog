from .app import app
from .config import config

app.config.from_mapping(config)

from .db import db  # noqa:  E402

# noinspection PyUnresolvedReferences
import models  # noqa: E402,F401
# noinspection PyUnresolvedReferences
import middlewares  # noqa: E402,F401
# noinspection PyUnresolvedReferences
import controllers  # noqa: E402,F401

db.create_all()

# noinspection PyUnresolvedReferences
import migrations  # noqa: E402,F401s
