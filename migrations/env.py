from logging.config import fileConfig
from sqlalchemy import pool  # noqa
from db import basic, DatabaseHelper
from alembic import context
import config as my_config


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# --- Импорты для сбора метаданных с моделей
import apps.user.models  # noqa
import apps.record.models  # noqa
target_metadata = basic.metadata


def get_url():
    return my_config.psql_url


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = DatabaseHelper().engine
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
