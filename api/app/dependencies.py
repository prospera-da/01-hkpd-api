from fastapi import Request

from .database import SessionLocal
from .utils.env_var import ENV


async def get_logger(request: Request):
    logger = request.app.state.logger
    yield logger

# Dependency
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()