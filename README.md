# Advent of Code

Repository of my code for [Advent of Code](https://adventofcode.com/)

## Install from github

Clone the repository and install the project in your python environment, either using `pip`

```bash
git clone git@github.com:jonasrenault/advent.git
cd advent
pip install --editable .
```

or [uv](https://docs.astral.sh/uv/)

```bash
git clone git@github.com:jonasrenault/advent.git
cd advent
uv sync
```

## Session

To get the code to work with your puzzle input, you need to be logged in using your session cookie. Log in to the [Advent of Code](https://adventofcode.com/) website and save your session cookie in a file called `.secret-session-cookie` in the project's root directory.

## Run

Each day's problem is solved in its own python module in a package corresponding to the year in the [advent](./advent/) directory. To run a solution, run

```bash
python advent/advent2023/day01.py
```

(prefix with `uv run` if using [uv](https://docs.astral.sh/uv/)).

## Usage

The [Advent](./advent/utils/utils.py) class in the `advent.utils.utils` module is used to get the input for a day's problem and submit solutions.

## Template generation

A CLI is provided to generate a blank template for a new day. Run

```bash
advent template [YEAR] [DAY]
```

(prefix with `uv run` if using [uv](https://docs.astral.sh/uv/)) and replace `[YEAR]` and `[DAY]` with the year and day you want to generate a template for.
