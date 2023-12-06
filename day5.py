# SPDX-License-Identifier: Unlicense

import sys
import re


def parse_map(buffer: list[str]):
    header = buffer.pop(0)

    m = {}
    source, destination = (s.removesuffix(" map:") for s in header.split("-to-"))
    m["destination"] = destination
    ranges = []

    while buffer:
        mapping = [int(x) for x in re.findall(r"\d+", buffer.pop(0))]
        if mapping:
            mapping = [mapping[1], mapping[2], mapping[0]]  # bring into sensible order, start, length, destination
            ranges.append(mapping)
        else:
            break

    m["ranges"] = sorted(ranges)  # this helps the iterative searcher a bit to decide if there are no more matches ahead
    return source, m


def build_maps(lines: list[str]):
    maps = {}
    buffer = [line for line in lines]
    while buffer:
        source, mapping = parse_map(buffer)
        maps[source] = mapping
    return maps


def remap(value: int, ranges: list[list[int]]) -> int:
    for source, length, destination in ranges:
        offset = value - source
        if 0 <= offset < length:
            value = destination + offset
            break
    return value


def resolve(value: int, step: str, maps: dict):
    while step in maps:
        m = maps[step]
        step = m["destination"]
        ranges = m["ranges"]
        value = remap(value, ranges)
    return value


def remap_range(workload: list[(int, int)], ranges: list[list[int]]) -> list[(int, int)]:
    results = []
    for start, span in workload:
        for source, length, destination in ranges:
            if span == 0:
                break

            if start < source:  # skip to first occurrence
                run = min(span, source - start)
                results.append((start, run))
                start += run
                span -= run

            offset = start - source
            if 0 <= offset < length:
                remaining = length - offset
                run = min(span, remaining)
                results.append((destination + offset, run))
                start += run
                span -= run

        if span > 0:
            results.append((start, span))

    return results


def resolve_range(start: int, span: int, step: str, maps: dict):
    workload = [(start, span)]

    while step in maps:
        m = maps[step]
        step = m["destination"]
        ranges = m["ranges"]
        workload = remap_range(workload, ranges)

    return min([s for s, _ in workload])


def actually_pairwise(iterable):
    pairwise = []
    for i in range(0, len(iterable), 2):
        pairwise.append((iterable[i], iterable[i+1]))
    return pairwise


def part_1(seeds: list[int], lines: list[str]):
    maps = build_maps(lines)

    locations = [resolve(seed, "seed", maps) for seed in seeds]
    print("Part 1", min(locations))


def part_2(seeds: list[(int, int)], lines: list[str]):
    maps = build_maps(lines)
    locations = [resolve_range(start, span, "seed", maps) for start, span in seeds]
    print("Part 2", min(locations))


def part_2_brute(seeds: list[(int, int)], lines: list[str]):
    maps = build_maps(lines)
    srs = [range(start, start+span) for start, span in seeds]
    locations = []
    for sr in srs:
        locations += [resolve(seed, "seed", maps) for seed in sr]
    print("Part 2", min(locations))


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        text = [line.strip() for line in f.readlines()]
        seed_data = [int(s) for s in re.findall(r"\d+", text.pop(0))]
        text.pop(0)  # consume empty line
        part_1(seed_data, text)
        seed_ranges = actually_pairwise(seed_data)
        part_2(seed_ranges, text)
