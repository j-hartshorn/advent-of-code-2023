from functools import reduce
from typing import Self

from pydantic import BaseModel


SYMBOLS = "*&#-@+/=$%"
DIGITS = "0123456789"


class Point(BaseModel):
    x: int
    y: int

    class Config:
        frozen: bool = True

    def adjacent_to(self, other: Self) -> bool:
        if abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1:
            return True


class Location(BaseModel):
    points: list[Point]

    class Config:
        frozen: bool = True

    def adjacent_to_point(self, point: Point) -> bool:
        for inner_point in self.points:
            if inner_point.adjacent_to(point):
                return True
        return False


class Part(BaseModel):
    value: int
    location: Location

    class Config:
        frozen: bool = True


class Gear(BaseModel):
    location: Point

    class Config:
        frozen: bool = True


def parse_parts(input_string: list[str]) -> list[Part]:
    character_grid = input_string.splitlines()
    part_list: list[Part] = []
    for row, line in enumerate(character_grid):
        reading_part_number = False
        for col, char in enumerate(line):
            if char in DIGITS:
                if not reading_part_number:
                    part_number = char
                    part_points = [Point(x=col, y=row)]
                    reading_part_number = True
                else:
                    part_number += char
                    part_points.append(Point(x=col, y=row))
            else:
                if reading_part_number:
                    part_list.append(
                        Part(
                            value=int(part_number),
                            location=Location(points=part_points),
                        )
                    )
                reading_part_number = False
        if reading_part_number:
            part_list.append(
                Part(value=int(part_number), location=Location(points=part_points))
            )
            reading_part_number = False
    return part_list


def parse_gears(input_string: list[str]) -> list[Gear]:
    character_grid = input_string.splitlines()
    gear_list: list[Gear] = []
    for row, line in enumerate(character_grid):
        for col, char in enumerate(line):
            if char == "*":
                gear_list.append(Gear(location=Point(x=col, y=row)))
    return gear_list


def collect_adjacent_parts(
    gear_list: list[Gear], part_list: list[Part]
) -> dict[Gear, list[Part]]:
    gear_adjacent_to: dict[Gear, list[Part]] = {}
    for gear in gear_list:
        gear_adjacent_to[gear] = []
        for part in part_list:
            if part.location.adjacent_to_point(gear.location):
                gear_adjacent_to[gear].append(part)
    gear_adjacent_to = {
        gear: part_list
        for gear, part_list in gear_adjacent_to.items()
        if len(part_list) == 2  # Filter for gears (exactly two adjacent parts)
    }
    return gear_adjacent_to


def total_gear_ratio(input_string: str) -> int:
    part_list = parse_parts(input_string)
    gear_list = parse_gears(input_string)
    gear_adjacent_to = collect_adjacent_parts(gear_list, part_list)
    gear_ratios: list[float] = [
        reduce(lambda x, y: x.value * y.value, part_list)
        for part_list in gear_adjacent_to.values()
    ]
    return sum(gear_ratios)


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

    assert total_gear_ratio(test_input) == 467835

    with open("python/day3/input.txt") as f:
        input_string = f.read()
        print(total_gear_ratio(input_string))
