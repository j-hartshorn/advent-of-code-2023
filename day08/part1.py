from enum import StrEnum
import re
from typing import Generator, Self

from pydantic import BaseModel, Field


class Move(StrEnum):
    LEFT = "L"
    RIGHT = "R"


def movement(movement_string: str) -> Generator[str, None, None]:
    length = len(movement_string)
    idx = 0
    while True:
        yield Move(movement_string[idx])
        idx += 1
        if idx >= length:
            idx = 0


class Location(BaseModel):
    location: str = Field(..., min_length=3, max_length=3)

    class Config:
        frozen: bool = True


class Network(BaseModel):
    network: dict

    @classmethod
    def from_string(cls, network_string: str) -> Self:
        edge_pattern = re.compile(r"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)")
        network = {}
        for line in network_string.splitlines():
            start, left, right = edge_pattern.match(line).groups()
            network[Location(location=start)] = {
                Move("L"): Location(location=left),
                Move("R"): Location(location=right),
            }
        return cls(network=network)

    def move(self, start: Location, move: Move) -> Location:
        return self.network[start][move]


def parse_input(input_string: str) -> tuple[str, dict[str, tuple[str, str]]]:
    movement_string, network_string = input_string.split("\n\n")

    return movement(movement_string), Network.from_string(network_string)


def count_steps_to_end(input_string: str) -> int:
    movement_gen, network = parse_input(input_string)
    start = Location(location="AAA")
    end = Location(location="ZZZ")
    location = start
    move_counter = 0
    for move in movement_gen:
        location = network.move(location, move)
        move_counter += 1
        if location == end:
            break
    return move_counter


if __name__ == "__main__":
    with open("day08/input_example_1.txt") as test_input:
        input_string = test_input.read()

    count_steps_to_end(input_string) == 2

    with open("day08/input_example_2.txt") as test_input:
        input_string = test_input.read()

    count_steps_to_end(input_string) == 6

    with open("day08/input.txt") as test_input:
        input_string = test_input.read()

    print(count_steps_to_end(input_string))
