import sys

words = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
cheese = ["z0o", "o1e", "t2o", "t3e", "f4r", "f5e", "s6", "s7n", "e8t", "n9e"]


def replace_words_with_digits(line: str):
    for i, word in enumerate(words):
        cheesy = cheese[i]
        line = line.replace(word, cheesy)
    return line


def value_lexical(line: str):
    line = replace_words_with_digits(line)
    digits = [d for d in line if d in "0123456789"]
    return int(digits[0] + digits[-1])


def value(line: str):
    digits = [d for d in line if d in "0123456789"]
    return int(digits[0] + digits[-1])


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()
        part1 = sum([value(x) for x in lines])
        print(part1)
        part2 = sum([value_lexical(x) for x in lines])
        print(part2)
