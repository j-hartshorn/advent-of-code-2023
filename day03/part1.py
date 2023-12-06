from collections import Counter
from dataclasses import dataclass

import numpy as np
from scipy.signal import convolve2d

SYMBOLS = "*&#-@+/=$%"
DIGITS = "0123456789"


def calculate_part_sum(input_string):
    characters = np.asarray([list(line) for line in input_string.splitlines()])

    symbol_mask = np.isin(characters, list(SYMBOLS))

    adjacency_filter = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
    symbol_ajacent = convolve2d(symbol_mask, adjacency_filter, mode="same") > 0

    n_row, n_col = characters.shape

    part_number_list = []
    for row in range(n_row):
        reading_part_number = False
        for col in range(n_col):
            char = characters[row, col]
            char_is_adjacent_to_symbol = symbol_ajacent[row, col]

            if char in DIGITS:
                if not reading_part_number:
                    part_number = char
                    part_is_adjacent_to_symbol = char_is_adjacent_to_symbol
                    reading_part_number = True
                else:
                    part_number += char
                    part_is_adjacent_to_symbol = (
                        char_is_adjacent_to_symbol or part_is_adjacent_to_symbol
                    )
            else:
                if reading_part_number and part_is_adjacent_to_symbol:
                    part_number_list.append(int(part_number))
                reading_part_number = False

        if reading_part_number and part_is_adjacent_to_symbol:
            part_number_list.append(int(part_number))
            reading_part_number = False

    return sum(part_number_list)


if __name__ == "__main__":
    test_input = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

    assert calculate_part_sum(test_input) == 4361

    with open("day03/input.txt") as f:
        input_string = f.read()
        print(calculate_part_sum(input_string))
