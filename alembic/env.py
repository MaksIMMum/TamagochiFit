# pylint: disable=method-hidden,no-member
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, event
from sqlalchemy.engine import Engine
from alembic import context
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import your models
from app.models import Base

config = context.config

# Get DATABASE_URL from environment variable
# This allows different databases for dev, test, production
database_url = os.getenv(
    "DATABASE_URL",
    "sqlite:///./tomogachifit.db"  # Default fallback
)

# Set the SQLAlchemy URL
config.set_main_option("sqlalchemy.url", database_url)

# Target metadata from SQLAlchemy models
target_metadata = Base.metadata

# SQLite-specific: Enable foreign key constraints
def receive_connect(dbapi_conn, connection_record):
    """Enable foreign key pragma for SQLite"""
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.StaticPool,
    )

    # Register SQLite pragma listener
    event.listen(Engine, "connect", receive_connect)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
