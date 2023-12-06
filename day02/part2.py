from collections import Counter
from functools import reduce
import re


def handful_from_string(handful_string: str) -> Counter:
    blocks_re = re.compile(r"(?:(\d+)\s(\w+),?)+")
    return Counter(
        {colour: int(count) for count, colour in blocks_re.findall(handful_string)}
    )


def minimun_colours(game: str) -> int:
    _, game_handful_string = game.split(":")
    handful_string_list = game_handful_string.split(";")
    handful_list = [handful_from_string(h) for h in handful_string_list]
    max_colours = reduce(lambda h1, h2: h1 | h2, handful_list)
    return max_colours


def calculate_power(min_colour: Counter) -> int:
    return reduce(lambda x, y: x * y, min_colour.values())


def calculate_total_power(games: str) -> int:
    legitimate_games = filter(lambda game: len(game) > 0, games.splitlines())
    min_colours = map(minimun_colours, legitimate_games)
    powers = map(calculate_power, min_colours)
    return sum(powers)


def test_calculate_total_power():
    test_input = """
    Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

    assert calculate_total_power(test_input) == 2286


if __name__ == "__main__":
    with open("day02/input.txt", "r") as f:
        print(calculate_total_power(f.read()))
