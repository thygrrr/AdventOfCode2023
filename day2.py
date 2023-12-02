import sys
import functools
import operator

bag = {"red": 12, "green": 13, "blue": 14}


def accumulate_draws(accumulator: dict[str, int], addition: dict[str, int]):
    for color, count in addition.items():
        current = accumulator.get(color, 0)
        if current < count:
            accumulator[color] = count


def parse_draws(turn: str) -> dict[str, int]:
    result = {}
    for draw in turn.split(", "):
        count, color = draw.split(" ")
        count = int(count)
        result[color] = count
    return result


def split_turns(game: str) -> list[str]:
    return game.split("; ")


def accumulate_game(line: str) -> (int, int):
    accumulator = {}
    game_id, game = line.split(": ")
    game_id = int(game_id.split(" ")[-1])
    turns = split_turns(game)
    for turn in turns:
        draws = parse_draws(turn)
        accumulate_draws(accumulator, draws)
    power = functools.reduce(operator.mul, accumulator.values(), 1)
    return game_id, power


def validate_game(line: str) -> (int, bool):
    game_id, game = line.split(": ")
    game_id = int(game_id.split(" ")[-1])
    turns = split_turns(game)
    for turn in turns:
        draws = parse_draws(turn)
        for color, count in draws.items():
            if color not in bag or bag[color] < count:
                return game_id, False
    return game_id, True



def part_1(entries: list[str]):
    total = 0
    for line in entries:
        game_id, ok = validate_game(line.strip())
        if ok:
            total += game_id

    print("Part 1:", total)


def part_2(entries: list[str]):
    total = 0
    for line in entries:
        game_id, power = accumulate_game(line.strip())
        total += power

    print("Part 2:", total)


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()
        part_1(lines)
        part_2(lines)
