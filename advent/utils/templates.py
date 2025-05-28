from pathlib import Path
from typing import Annotated

import typer
from jinja2 import Environment, FileSystemLoader

app = typer.Typer()


def generate_day(day: int, year: int, output_dir: Path):
    env = Environment(loader=FileSystemLoader("templates"), autoescape=True)
    template = env.get_template("day.py")

    fn = output_dir / f"day{day:02d}.py"
    if not fn.exists():
        with open(fn, "w") as f:
            f.write(template.render(day=day, year=year))


@app.command()
def template(
    year: Annotated[
        int,
        typer.Argument(
            help="Year to generate a template for.",
        ),
    ] = 2025,
    day: Annotated[
        int,
        typer.Argument(
            help="Day to generate a template for.",
        ),
    ] = 1,
    all: Annotated[bool, typer.Option(help="Generate all days for the year.")] = False,
    output: Annotated[str, typer.Option(help="The output directory.")] = "advent",
):
    output_dir = Path(output) / f"advent{year}"
    output_dir.mkdir(exist_ok=True)
    if all:
        for d in range(1, 26):
            generate_day(d, year, output_dir)
    else:
        generate_day(day, year, output_dir)
