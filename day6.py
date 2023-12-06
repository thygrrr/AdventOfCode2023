# SPDX-License-Identifier: Unlicense

import math
import re
import sys
from functools import reduce


def get_min_max(time: int, distance: int) -> (int, int):
    x1 = time/2 - math.sqrt(time**2 - 4*distance)/2
    x2 = time/2 + math.sqrt(time**2 - 4*distance)/2
    return math.ceil(x1), math.floor(x2)


def margin(time: int, distance: int) -> int:
    mn, mx = get_min_max(time, distance)
    return mx - mn + 1


def part_1(times: list[int], distances: list[int]):
    margins = [margin(time, distance) for time, distance in zip(times, distances)]
    print("Part 1:", reduce(lambda a, b: a * b, margins))
    pass


def part_2(times: list[int], distances: list[int]):
    margins = [margin(time, distance) for time, distance in zip(times, distances)]
    print("Part 2:", reduce(lambda a, b: a * b, margins))


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        time_data = [int(t) for t in re.findall(r"\d+", f.readline())]
        distance_data = [int(d) for d in re.findall(r"\d+", f.readline())]
        part_1(time_data, distance_data)

    with open(sys.argv[1]) as f:
        time_data = [int(t) for t in re.findall(r"\d+", f.readline().replace(" ", ""))]
        distance_data = [int(d) for d in re.findall(r"\d+", f.readline().replace(" ", ""))]
        part_2(time_data, distance_data)
