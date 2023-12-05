import sys
import re


def parse_map(buffer: list[str]):
    header = buffer.pop(0)
    m = {}
    ranges = []
    source, destination = (s.removesuffix(" map:") for s in header.split("-to-"))
    m["destination"] = destination
    m["ranges"] = ranges

    while buffer:
        mapping = [int(x) for x in re.findall(r"\d+", buffer.pop(0))]
        if mapping:
            ranges.append(mapping)
        else:
            break

    return source, m


def build_maps(lines: list[str]):
    maps = {}
    buffer = [line for line in lines]
    while buffer:
        source, mapping = parse_map(buffer)
        maps[source] = mapping
    return maps


def remap(value: int, ranges: list[list[int]]) -> int:
    for source, destination, length in ranges:
        offset = value-source
        if 0 <= offset < length:
            value = destination + offset
            break
    return value


def resolve(value: int, step: str, maps: dict):
    print("---")
    print(step)
    while step in maps:
        m = maps[step]
        step = m["destination"]
        ranges = m["ranges"]
        print(step)
        value = remap(value, ranges)
    return value


def part_1(seeds: list[int], lines: list[str]):
    maps = build_maps(lines)

    locations = [resolve(seed, "seed", maps) for seed in seeds]
    print("Part 1", min(locations))


def part_2(seeds: list[int], lines: list[str]):
    pass


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        text = [line.strip() for line in f.readlines()]
        seed_data = [int(s) for s in re.findall(r"\d+", text.pop(0))]
        text.pop(0)  # consume empty line
        part_1(seed_data, text)
        part_2(seed_data, text)
