from pathlib import Path

import click
from jinja2 import Environment, FileSystemLoader


def generate_day(day: int, output_dir: Path):
    env = Environment(loader=FileSystemLoader("templates"), autoescape=True)
    template = env.get_template("day.py")

    fn = output_dir / f"day{day:02d}.py"
    if not fn.exists():
        with open(fn, "w") as f:
            f.write(template.render(day=day))


@click.command()
@click.option("-d", "--day", default=1, help="day to generate")
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
    default="advent/advent2022",
    type=click.Path(dir_okay=True),
)
def day(day: int, all: bool, output: str):
    if all:
        for d in range(1, 26):
            generate_day(d, Path(output))
    else:
        generate_day(day, Path(output))


if __name__ == "__main__":
    day()
