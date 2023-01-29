import typer
import uvicorn

from migrations import migrations

cli = typer.Typer()


@cli.command()
def db_upgrade():
    migrations.upgrade()


@cli.command()
def db_downgrade():
    migrations.downgrade()


@cli.command()
def db_make_migration(msg: str, autogenerate: bool = False):
    migrations.make_migration(msg, autogenerate=autogenerate)


@cli.command()
def run(
    host: str = typer.Option("0.0.0.0", envvar="API_HOST"),
    port: int = typer.Option(8000, envvar="API_PORT"),
    workers: int = typer.Option(1, envvar="API_WORKERS"),
    debug: bool = typer.Option(False, envvar="DEBUG"),
):
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
