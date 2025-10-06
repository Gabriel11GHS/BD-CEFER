import os
import sys

# Ensure project root is on sys.path so tests can import top-level modules
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest
from dbsession import DBSession


@pytest.fixture
def dbsession():
    """Create a `tests` schema, yield a DBSession bound to it, and drop the schema on teardown.

    Shared fixture for tests that need a DBSession scoped to the `tests` schema.
    """
    # ensure clean state - drop schema if it exists
    with DBSession() as db:
        with db.connection.cursor() as cur:
            cur.execute("DROP SCHEMA IF EXISTS tests CASCADE;")
            db.connection.commit()

    # create fresh schema
    with DBSession() as db:
        with db.connection.cursor() as cur:
            cur.execute("CREATE SCHEMA IF NOT EXISTS tests;")
            db.connection.commit()

    # create session and yield it
    session = DBSession(schema='tests')
    try:
        yield session
    finally:
        session.close()
        with DBSession() as db:
            with db.connection.cursor() as cur:
                cur.execute("DROP SCHEMA IF EXISTS tests CASCADE;")
                db.connection.commit()
