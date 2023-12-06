def number_from_line(line: str) -> int:
    numbers_in_line = [c for c in line if c.isdigit()]
    if len(numbers_in_line) < 1:
        return None
    return int("".join([numbers_in_line[0], numbers_in_line[-1]]))


def retrieve_calibration(input: str) -> list[int]:
    lines = input.splitlines()
    return sum(map(number_from_line, lines))


def test_number_from_line():
    assert number_from_line("b2r98f2yg") == 22
    assert number_from_line("hd83yb57w42jrf75") == 85
    assert number_from_line("jdurgvfkvd") == None
    assert number_from_line("0987654321") == 1


def test_retrieve_calibration():
    test_input = """1abc2
    pqr3stu8vwx
    a1b2c3d4e5f
    treb7uchet"""

    assert retrieve_calibration(test_input) == sum([12, 38, 15, 77])


if __name__ == "__main__":
    with open("day01/input.txt", "r") as f:
        print(retrieve_calibration(f.read()))
