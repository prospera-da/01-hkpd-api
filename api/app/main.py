from fastapi import FastAPI

from .database import engine, Base
from .routers import akun

Base.metadata.create_all(bind=engine)

import logging

# Create a logger object
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)


app = FastAPI()

app.state.logger = logger

app.include_router(akun.router)
