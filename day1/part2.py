def replace_numbers_with_digits(line: str) -> str:
    number_strings = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
        "zero": "0",
    }
    i = 0
    out_line = ""
    check_overlap = False
    while i < len(line):
        match_found = False
        for number_string, digit in number_strings.items():
            number_length = len(number_string)
            sub_line = line[i : i + number_length]
            if i + number_length - 1 > len(line):
                # Not enough letters left to match
                continue
            if sub_line == number_string:
                out_line += digit
                i += number_length
                match_found = True
                check_overlap = True
                break
            # Got to check one letter back in the case that the previous step matched a number
            sub_line_lookback = line[i - 1 : i - 1 + number_length]
            if check_overlap and (sub_line_lookback == number_string):
                out_line += digit
                i += number_length - 1
                match_found = True
                break
        if not match_found:
            out_line += line[i]
            i += 1
            check_overlap = False
    return out_line


def number_from_line(line: str) -> int:
    line = replace_numbers_with_digits(line)
    numbers_in_line = [c for c in line if c.isdigit()]
    if len(numbers_in_line) < 1:
        return 0
    return int("".join([numbers_in_line[0], numbers_in_line[-1]]))


def retrieve_calibration(input: str) -> list[int]:
    lines = input.splitlines()
    return sum(map(number_from_line, lines))


def test_replace_numbers_with_digits():
    assert replace_numbers_with_digits("one") == "1"
    assert replace_numbers_with_digits("two1gfyithree486e") == "21gfyi3486e"
    assert replace_numbers_with_digits("twone5") == "215"


def test_number_from_line():
    assert number_from_line("b2r98f2one") == 21
    assert number_from_line("hd83yb57w42jrf75") == 85
    assert number_from_line("jdurgvfkvd") == 0
    assert number_from_line("0987654321") == 1


def test_retrieve_calibration():
    test_input = """1abc2
    pqr3stu8vwx
    a1b2c3d4e5f
    treb7uchet"""

    assert retrieve_calibration(test_input) == sum([12, 38, 15, 77])

    part_2_test_input = """two1nine
    eightwothree
    abcone2threexyz
    xtwone3four
    4nineeightseven2
    zoneight234
    7pqrstsixteen"""

    assert retrieve_calibration(part_2_test_input) == sum([29, 83, 13, 24, 42, 14, 76])


if __name__ == "__main__":
    with open("day1/input.txt", "r") as f:
        print(retrieve_calibration(f.read()))
