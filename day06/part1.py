from math import prod


def number_of_winning_strategies(race_time: int, race_distance: int) -> int:
    winning_attemps = 0
    for button_held_time in range(1, race_time):
        speed = button_held_time
        attempt_race_time = race_distance / speed + button_held_time
        is_winning = attempt_race_time < float(race_time)
        if is_winning:
            winning_attemps += 1
    return winning_attemps


def product_of_strategies(races: tuple[int, int]) -> int:
    return prod(number_of_winning_strategies(*race) for race in races)


if __name__ == "__main__":
    # Test cases
    assert number_of_winning_strategies(race_time=7, race_distance=9) == 4
    assert number_of_winning_strategies(race_time=15, race_distance=40) == 8
    assert number_of_winning_strategies(race_time=30, race_distance=200) == 9

    races = [
        (7, 9),
        (15, 40),
        (30, 200),
    ]
    assert product_of_strategies(races) == 288

    races = [(35, 213), (69, 1168), (68, 1086), (87, 1248)]

    print(product_of_strategies(races))
