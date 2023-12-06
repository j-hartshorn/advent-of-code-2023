from numba import njit


@njit
def number_of_winning_strategies(race_time: int, race_distance: int) -> int:
    winning_attemps = 0
    for button_held_time in range(1, race_time):
        speed = button_held_time
        attempt_race_time = race_distance / speed + button_held_time
        is_winning = attempt_race_time < float(race_time)
        if is_winning:
            winning_attemps += 1
    return winning_attemps


if __name__ == "__main__":
    race_time = 35696887
    race_distance = 213116810861248

    print(
        number_of_winning_strategies(race_time=race_time, race_distance=race_distance)
    )
