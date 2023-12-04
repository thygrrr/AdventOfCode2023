import sys


def calc_score(win: str, num: str) -> int:
    winners = {int(w) for w in win.split(" ") if w}
    numbers = {int(n) for n in num.split(" ") if n}
    matches = numbers.intersection(winners)

    count = len(matches)
    return 2 ** (count - 1) if count else 0


def score_line(line: str) -> int:
    card, numbers = line.split(": ")
    winners, scratches = numbers.split(" | ")
    return calc_score(winners, scratches)


def part_1(lines: list[str]):
    scores = [score_line(l) for l in lines]
    print("Part 1", sum(scores))


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        text = [line.strip() for line in f.readlines()]
        part_1(text)
