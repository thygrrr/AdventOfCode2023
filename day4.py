# SPDX-License-Identifier: Unlicense

import sys
import re


def count_matches(win: str, num: str) -> int:
    winners = {int(w) for w in re.findall(r"\d+", win)}
    numbers = {int(n) for n in re.findall(r"\d+", num)}
    matches = numbers.intersection(winners)
    return len(matches)


def score_line(count: int) -> int:
    return 2 ** (count - 1) if count else 0


def match_line(line: str) -> int:
    card, numbers = line.split(": ")
    winners, scratches = numbers.split(" | ")
    return count_matches(winners, scratches)


def part_1(lines: list[str]):
    scores = [score_line(match_line(line)) for line in lines]
    print("Part 1", sum(scores))


def part_2(lines: list[str]):
    numbered = [[line] for line in lines]
    completed = []
    while numbered:
        batch = numbered.pop(0)
        completed.append(batch)
        matches = match_line(batch[0])
        for m in range(min(matches, len(numbered))):
            numbered[m] += [numbered[m][0]] * len(batch)

    cards = sum([len(batch) for batch in completed])
    print("Part 2", cards)


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        text = [line.strip() for line in f.readlines()]
        part_1(text)
        part_2(text)
