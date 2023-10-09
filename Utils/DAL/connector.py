from contextlib import contextmanager
from contextvars import ContextVar

from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import DeclarativeBase, Session

# Base class for MySQL database models and session management
class MySQLBase(DeclarativeBase):
    _session_context: ContextVar[Session] = ContextVar("_session_object", default=None)

    _engine: Engine = None
    __abstract__ = True

    @classmethod
    def set_session(cls, session: Session):
        return cls._session_context.set(session)

    @classmethod
    def get_session(cls):
        return cls._session_context.get() or Session(cls._engine)

    @classmethod
    @contextmanager
    def managed_session(cls):
        session = Session(cls._engine)
        token = cls.set_session(session)

        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

            # reset the _session_object to previous object
            cls._session_context.reset(token)

    @classmethod
    def query(cls, *args, **kwargs):
        session = cls.get_session()
        if not args and not kwargs:
            query = session.query(cls)
        else:
            query = session.query(*args, **kwargs)
        return query
