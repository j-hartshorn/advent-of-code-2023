from collections import Counter
from functools import reduce
import re


BAG_CONTENTS = Counter(
    {
        "red": 12,
        "green": 13,
        "blue": 14,
    }
)


def handful_from_string(handful_string: str) -> Counter:
    blocks_re = re.compile(r"(?:(\d+)\s(\w+),?)+")
    return Counter(
        {colour: int(count) for count, colour in blocks_re.findall(handful_string)}
    )


def game_score(game: str) -> int:
    index_string, game_handful_string = game.split(":")
    index = int(index_string[5:])
    handful_string_list = game_handful_string.split(";")
    handful_list = [handful_from_string(h) for h in handful_string_list]
    max_colours = reduce(lambda h1, h2: h1 | h2, handful_list)
    if BAG_CONTENTS > max_colours:
        return index
    else:
        return 0


def total_score(games: str) -> int:
    return sum(game_score(game) for game in games.splitlines() if len(game) > 0)


if __name__ == "__main__":
    with open("python/day2/input.txt", "r") as f:
        print(total_score(f.read()))
