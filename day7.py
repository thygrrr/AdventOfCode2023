# SPDX-License-Identifier: Unlicense

import sys
from collections import Counter

card_ranks = "23456789TJQKA"

card_ranks_wild = "J23456789TQKA"


def hand_key(scored: (int, str, int)):  # points value (better hand = higher), hand, bid (ignored)
    points, hand, _ = scored
    for card in hand:
        points *= 100
        points += card_ranks.index(card)
    return points


def hand_key_wild(scored: (int, str)):
    points, hand, _ = scored
    for card in hand:
        points *= 100
        points += card_ranks_wild.index(card)
    return points


def score(hand: str) -> (int, int):
    counter = Counter(hand)
    squares = [x * x for x in counter.values()]
    scored = sum(squares)
    return scored, hand


def score_wild(hand: str) -> (int, int):
    counter = Counter(hand)
    jacks = counter['J']
    del counter['J']

    # else [0] means ALL JACKS! So we need to recreate a group to add the no. of jacks to.
    values = sorted(counter.values(), reverse=True) if len(counter) else [0]
    values[0] += jacks  # Make the largest group larger by number of wildcards (jacks)

    squares = [x * x for x in values]
    scored = sum(squares)
    return scored, hand


def part_1(hands: list[(str, int)]):
    scored = [score(hand) + (bid,) for hand, bid in hands]
    winnings = []
    for index, entry in enumerate(sorted(scored, key=hand_key)):
        _, _, bid = entry
        winnings.append((index + 1) * bid)
    print("Part 1:", sum(winnings))


def part_2(hands: list[(str, int)]):
    scored = [score_wild(hand) + (bid,) for hand, bid in hands]
    winnings = []
    for index, entry in enumerate(sorted(scored, key=hand_key_wild)):
        _, _, bid = entry
        winnings.append((index + 1) * bid)
    print("Part 2:", sum(winnings))


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        text = [line.strip().split(" ") for line in f]
        hand_data = [(hand, int(bid)) for hand, bid in text]
        part_1(hand_data)
        part_2(hand_data)
