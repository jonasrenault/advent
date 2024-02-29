from pathlib import Path

import click
from jinja2 import Environment, FileSystemLoader


def generate_day(day: int, year: int, output_dir: Path):
    env = Environment(loader=FileSystemLoader("templates"), autoescape=True)
    template = env.get_template("day.py")

    fn = output_dir / f"day{day:02d}.py"
    if not fn.exists():
        with open(fn, "w") as f:
            f.write(template.render(day=day, year=year))


@click.command()
@click.option("-d", "--day", default=1, help="day to generate")
@click.option("-y", "--year", default=2022, help="year to generate")
@click.option(
    "-a",
    "--all",
    default=False,
    help="generate all days",
    is_flag=True,
)
@click.option(
    "-o",
    "--output",
    help="the output dir",
    default="advent",
    type=click.Path(dir_okay=True),
)
def day(day: int, year: int, all: bool, output: str):
    output_dir = Path(output) / f"advent{year}"
    output_dir.mkdir(exist_ok=True)
    if all:
        for d in range(1, 26):
            generate_day(d, year, output_dir)
    else:
        generate_day(day, year, output_dir)


if __name__ == "__main__":
    day()
