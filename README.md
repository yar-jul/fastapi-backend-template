# fastapi-backend-template

A Python backend template with FastAPI, PostgreSQL, asynchronous SQLAlchemy, Alembic, Pytest, Docker, GitHub Actions,
pgAdmin and Poetry.

## Requirements

- Python 3.10
- Poetry
- Docker
- Docker Compose

# Installation

```bash
git clone git@github.com:yar-jul/fastapi-backend-template.git
cd fastapi-backend-template/backend
poetry install
```

You can also activate the vernal environment. On Unix:

```bash
source .venv/bin/activate
```

To run app in docker-compose:

```bash
cd fastapi-backend-template
make install
```

To populate the database with test data:

```bash
cd fastapi-backend-template/backend
make populate-db
```

# Usage

<div class="termy">

```console
$ cd fastapi-backend-template/backend
$ apicli --help
Usage: apicli [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  db-downgrade       downgrade migrations
  db-make-migration  make migration.
  db-upgrade         upgrade migrations
  run                run api
```

</div>

Open API docs in your browser to <http://localhost:8000/docs>  
Open pgAdmin in your browser to <http://localhost:5050>
