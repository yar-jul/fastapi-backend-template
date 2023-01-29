from pathlib import Path

from alembic import command
from alembic.config import Config

migrations_path = Path(__file__).parent
config_filepath = migrations_path / Path("alembic.ini")

config = Config(config_filepath.as_posix())
config.set_main_option("script_location", migrations_path.as_posix())


def upgrade():
    print(config_filepath)
    command.upgrade(config, revision="head")


def downgrade():
    command.downgrade(config, revision="-1")


def make_migration(message: str, autogenerate: bool):
    command.revision(config, message=message, autogenerate=autogenerate)
