import logging

import typer
from rich.logging import RichHandler

from advent.utils.templates import app as template_app

FORMAT = "%(message)s"
logging.basicConfig(
    level=logging.INFO, format=FORMAT, datefmt="[%X]", handlers=[RichHandler(markup=True)]
)

app = typer.Typer(no_args_is_help=True)

app.add_typer(template_app)

if __name__ == "__main__":
    app()
