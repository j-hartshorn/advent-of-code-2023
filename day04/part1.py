def parse_line(line):
    _, numbers_string = line.split(":")
    winning_numbers_str, chosen_numbers_str = numbers_string.split("|")
    winning_numbers = [int(x) for x in winning_numbers_str.split()]
    chosen_numbers = [int(x) for x in chosen_numbers_str.split()]
    return winning_numbers, chosen_numbers


def count_winning_numbers(winning_numbers, chosen_numbers):
    return sum(n in winning_numbers for n in chosen_numbers)


def points_per_match(matches: int) -> int:
    return 1 * int(2 ** (matches - 1))


def total_points(input_string: str) -> int:
    parsed_input = [parse_line(line) for line in input_string.splitlines()]
    return sum(
        points_per_match(count_winning_numbers(winning_numbers, chosen_numbers))
        for winning_numbers, chosen_numbers in parsed_input
    )


if __name__ == "__main__":
    test_input = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
    Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
    Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
    Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
    Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

    assert total_points(test_input) == 13

    with open("day04/input.txt") as f:
        input_string = f.read()
        print(total_points(input_string))
