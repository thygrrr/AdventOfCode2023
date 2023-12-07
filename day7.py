import sys
import re
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
    values = counter.values()
    squares = map(lambda x: x * x, values)
    scored = sum(squares)
    return scored, hand


def score_wild(hand: str) -> (int, int):
    counter = Counter(hand)
    jacks = counter['J']
    del counter['J']

    values = sorted(counter.values(), reverse=True)

    if not values:
        values = [0]  # ALL JACKS! So we need to reserve a slot to add the count of jacks to.

    values[0] += jacks  # Make the largest group larger by number of jacks

    squares = map(lambda x: x * x, values)
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
        text = [line.strip().split(" ") for line in f.readlines()]
        hand_data = [(hand, int(bid)) for hand, bid in text]
        part_1(hand_data)
        part_2(hand_data)
