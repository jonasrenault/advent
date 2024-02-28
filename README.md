# Advent of Code 2022

Repository of my code for [Advent of Code](https://adventofcode.com/)

## Install

Install project with its dependencies with [poetry](https://python-poetry.org/):

```console
poetry install
```

## Session

To get the code to work with your puzzle input, you need to be logged in using your session cookie. Log in to the [Advent of Code](https://adventofcode.com/) website and save your session cookie in a file called `.secret-session-cookie` in the project's root directory.

## Run

Each day's problem is solved in its own python module in a package corresponding to the year in the [advent](./advent/) directory. To run a solution, run

```console
poetry run python advent/advent2023/day01.py
```

## Template generation

To generate a blank template for a new day, a template generator can be used with

```console
poetry run python advent/utils/templates.py -y 2023 -d 1
```

where the `-y` option specifies the year and `-d` specifies the day to generate a template for.
