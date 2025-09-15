import functools
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError

def db_exception_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        db = None
        if args and isinstance(args[0], Session):
            db = args[0]

        try:
            return func(*args, **kwargs)
        except IntegrityError as e:
            if db:
                db.rollback()
            raise HTTPException(status_code=400, detail="Database integrity error: " + str(e.orig))
        except OperationalError as e:
            if db:
                db.rollback()
            raise HTTPException(status_code=500, detail="Database operational error: " + str(e.orig))
        except SQLAlchemyError as e:
            if db:
                db.rollback()
            raise HTTPException(status_code=500, detail="Database error: " + str(e))
    return wrapper