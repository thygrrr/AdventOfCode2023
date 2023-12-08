import sys
import re
import functools
from sympy.ntheory import factorint as factors


def parse(line: str):
    key, left, right = re.findall("[A-Z]+", line)
    return key, (left, right)


def parse_maps(f):
    maps = {}
    for line in f:
        key, lr = parse(line)
        maps[key] = lr
    return maps


def count_steps(directions: str, maps: dict[str, (str, str)], start: str) -> int:
    location = start

    choices = None
    steps = 0
    while not location.endswith("Z"):
        steps += 1

        if not choices:
            choices = [c for c in directions]
            choices.reverse()

        choice = choices.pop()
        left, right = maps[location]

        if choice == 'L':
            location = left
        else:
            location = right

    return steps


def part_2(directions: str, maps: dict[str, (str, str)]):
    locations = {loc for loc in filter(lambda d: d.endswith("A"), maps.keys())}
    steps = [count_steps(directions, maps, location) for location in locations]
    primes = set()
    for step in steps:
        primes |= factors(step).keys()

    multiples = functools.reduce(lambda x, y: x * y, primes)

    print("Part 2:", multiples)


def part_1(directions: str, maps: dict[str, (str, str)]):
    location = "AAA"

    choices = None
    steps = 0
    while location != "ZZZ":
        steps += 1

        if not choices:
            choices = [c for c in directions]
            choices.reverse()

        choice = choices.pop()
        left, right = maps[location]

        if choice == 'L':
            location = left
        else:
            location = right

    print("Part 1:", steps)


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        dirs = f.readline().strip()
        f.readline()
        data = parse_maps(f)
        part_1(dirs, data)
        part_2(dirs, data)
