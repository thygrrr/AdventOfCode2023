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
    for r in range(row-1, row+2):
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
    for r in range(row-1, row+2):
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


def stars_for_numbers(data: list[(int, list[(int, int)])]) -> dict[(int, int), list[int]]:
    lookup: dict[(int, int), list[int]] = {}
    for item in data:
        number, coordinates = item
        for coord in coordinates:
            if coord in lookup:
                lookup[coord].append(number)
            else:
                lookup[coord] = [number]
    return lookup


def part_1(lines: list[str]):
    part_nums = find_numbers_with_symbols(lines)
    print("Part 1:", sum(part_nums))


def part_2(lines: list[str]):
    lookup = stars_for_numbers(find_numbers_with_stars(lines)).items()
    gears = [(coord, numbers) for coord, numbers in lookup if len(numbers) == 2]
    ratios = [g[0] * g[1] for _, g in gears]
    print("Part 2:", sum(ratios))


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        text = [line.strip() for line in f.readlines()]
        part_1(text)
        part_2(text)
