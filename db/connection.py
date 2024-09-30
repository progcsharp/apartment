__all__ = ['make_session']

import sys

from sqlalchemy.orm import sessionmaker

from .engine import engine


def make_session():
    try:
        print("Create transaction...")
        _engine = engine()
        _Session = sessionmaker(bind=_engine)
        session = _Session()
        print("Transaction created!")
        return session
    except:
        print(f"Couldn't create transaction!"
              f"Check log's: {sys.exc_info()}")
        raise sys.exc_info()

