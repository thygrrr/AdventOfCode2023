import re
import sys
from itertools import pairwise


def extrapolate(values: list[int]):
    deltas = [b - a for a, b in pairwise(values)]
    if any(deltas):
        return values[-1] + extrapolate(deltas)
    return values[-1]


def extrapolate_backwards(values: list[int]):
    deltas = [b - a for a, b in pairwise(values)]
    if any(deltas):
        return values[0] - extrapolate_backwards(deltas)
    return values[0]


def part_1(values: list[list[int]]):
    result = sum([extrapolate(line) for line in values])
    print("Part 1:", result)


def part_2(values: list[list[int]]):
    result = sum([extrapolate_backwards(line) for line in values])
    print("Part 2:", result)


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        readings = [[int(num) for num in re.findall(r"-?\d+", line)] for line in f]
        part_1(readings)
        part_2(readings)
