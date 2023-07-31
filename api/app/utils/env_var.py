import os

ENV = os.getenv("ENVIRONMENT", "dev")

# Tracking constants
MODEL_VERSION = os.getenv("MODEL_VERSION") or "manual"
MODEL_NAME = os.getenv("MODEL_NAME")
AUTH0_TRACKING_AUDIENCE = os.getenv("AUTH0_TRACKING_AUDIENCE")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")

# Database constants
DATABASE_HOST = os.getenv("DATABASE_HOST")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_USER = os.getenv("MYSQL_USER")
