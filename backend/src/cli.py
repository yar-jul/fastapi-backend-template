import typer
import uvicorn

from migrations import migrations

cli = typer.Typer()


@cli.command()
def db_upgrade():
    """upgrade migrations"""
    migrations.upgrade()


@cli.command()
def db_downgrade():
    """downgrade migrations"""
    migrations.downgrade()


@cli.command()
def db_make_migration(msg: str, autogenerate: bool = False):
    """
    make migration.

    export SQLALCHEMY_DATABASE_DSN=...
    apicli db-make-migration --autogenerate msg
    """
    migrations.make_migration(msg, autogenerate=autogenerate)


@cli.command()
def run(
    host: str = typer.Option("0.0.0.0", envvar="API_HOST"),
    port: int = typer.Option(8000, envvar="API_PORT"),
    workers: int = typer.Option(1, envvar="API_WORKERS"),
    debug: bool = typer.Option(False, envvar="DEBUG"),
):
    """run api"""
    log_level = "info"
    if debug:
        log_level = "debug"

    uvicorn.run(
        "api.app.app:create_app",
        factory=True,
        host=host,
        port=port,
        workers=workers,
        reload=debug,
        log_level=log_level,
    )


if __name__ == "__main__":
    cli()
