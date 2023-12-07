# SPDX-License-Identifier: Unlicense

import sys
import re


def symbols_in_range(array: list[str], span: (int, int), row: int) -> set[str]:
    if row < 0 or row >= len(array):
        return set()

    line = array[row]
    start, end = span
    if start > 0:
        start -= 1
    end += 1
    return {s for s in line[start:end] if not s.isdigit() and s != '.'}


def collect_adjacent_symbols(array: list[str], span: (int, int), row: int) -> set[str]:
    symbols = set()
    for r in range(row - 1, row + 2):
        symbols |= symbols_in_range(array, span, r)
    return symbols


def stars_in_range(array: list[str], span: (int, int), row: int) -> set[(int, int)]:
    if row < 0 or row >= len(array):
        return set()

    line = array[row]
    start, end = span
    if start > 0:
        start -= 1
    if end < len(line):
        end += 1

    stars = set()
    for i in range(start, end):
        if line[i] == '*':
            stars.add((i, row))

    return stars


def collect_adjacent_stars(array: list[str], span: (int, int), row: int) -> set[(int, int)]:
    stars = set()
    for r in range(row - 1, row + 2):
        stars |= stars_in_range(array, span, r)
    return stars


def find_numbers_with_symbols(array: list[str]) -> list[int]:
    numbers = []
    for l, line in enumerate(array):
        matches = re.finditer(r"\d+", line)
        for match in matches:
            symbols = collect_adjacent_symbols(array, match.span(), l)
            if symbols:
                numbers.append(int(match.group()))

    return numbers


def find_numbers_with_stars(array: list[str]) -> list[(int, list[(int, int)])]:
    numbers_and_stars = []
    for l, line in enumerate(array):
        matches = re.finditer(r"\d+", line)
        for match in matches:
            stars = collect_adjacent_stars(array, match.span(), l)
            if stars:
                data = (int(match.group()), stars)
                numbers_and_stars.append(data)

    return numbers_and_stars


def find_all_stars(array: list[str]) -> list[(int, int, int)]:
    numbers = []
    for index, line in enumerate(array):
        for match in re.finditer(r"\*", line):
            span = match.span()
            numbers.append((span[0], index))
    return numbers


def find_all_numbers(array: list[str]) -> list[(int, (int, int, int))]:
    numbers = []
    for row, line in enumerate(array):
        for match in re.finditer(r"\d+", line):
            span = match.span()
            numbers.append((int(match.group()), (span[0], span[1], row)))
    return numbers


def stars_for_numbers(data: list[(int, list[(int, int)])]) -> dict[(int, int), list[int]]:
    lookup: dict[(int, int), list[int]] = {}
    for item in data:
        number, coordinates = item
        for coord in coordinates:
            lookup.setdefault(coord, []).append(number)
    return lookup


def stars_for_numbers_alt(numbers: list[(int, (int, int, int))], stars: list[(int, int)]) -> dict[(int, int), list[int]]:
    lookup: dict[(int, int), list[int]] = {}
    for number, coordinates in numbers:
        start, end, row = coordinates
        for position in stars:
            column, line = position
            if (line - 1 <= row <= line + 1) and (start - 1 <= column < end + 1):  # this part is disgusting
                lookup.setdefault(position, []).append(number)

    return lookup


def part_1(lines: list[str]):
    part_nums = find_numbers_with_symbols(lines)
    print("Part 1:", sum(part_nums))


def part_2(lines: list[str]):
    lookup = stars_for_numbers(find_numbers_with_stars(lines)).items()
    gears = [(coord, numbers) for coord, numbers in lookup if len(numbers) == 2]
    ratios = [g[0] * g[1] for _, g in gears]
    print("Part 2:", sum(ratios))


def part_2_alt(lines: list[str]):
    numbers = find_all_numbers(lines)
    stars = find_all_stars(lines)
    lookup = stars_for_numbers_alt(numbers, stars).items()
    gears = [(coord, numbers) for coord, numbers in lookup if len(numbers) == 2]
    ratios = [g[0] * g[1] for _, g in gears]
    print("Part 2 alt:", sum(ratios))


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        text = [line.strip() for line in f.readlines()]
        part_1(text)
        part_2(text)
        part_2_alt(text)
