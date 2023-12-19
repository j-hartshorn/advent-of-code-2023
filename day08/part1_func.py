from enum import StrEnum
import re
from typing import Callable, Generator, Self

from pydantic import BaseModel, Field


def movement_generator(movement_string: str) -> Generator[str, None, None]:
    length = len(movement_string)
    idx = 0
    while True:
        yield movement_string[idx]
        idx += 1
        if idx >= length:
            idx = 0


def parse_network(network_string: str) -> dict[str, tuple[str, str]]:
    edge_pattern = re.compile(r"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)")
    network = {}
    for line in network_string.splitlines():
        start, left, right = edge_pattern.match(line).groups()
        network[start] = (left, right)
    return network


def parse_input(
    input_string: str,
) -> tuple[Generator[str, None, None], dict[str, tuple[str, str]]]:
    movement_string, network_string = input_string.split("\n\n")
    return movement_generator(movement_string), parse_network(network_string)


def create_step(network: dict[str, tuple[str, str]]) -> Callable[[str, str], str]:
    def step(start_location: str, move: str) -> str:
        directions = network[start_location]
        match move:
            case "L":
                return directions[0]
            case "R":
                return directions[1]
            case _:
                raise ValueError(f"Unknown direction {move}")

    return step


def count_steps_to_end(
    moves: Generator[str, None, None],
    network: dict[str, tuple[str, str]],
    start_location: str = "AAA",
    end_location: str = "ZZZ",
) -> int:
    step = create_step(network=network)
    step_count = 0
    location = start_location
    for move in moves:
        location = step(location, move)
        step_count += 1
        if location == end_location:
            break
    return step_count


if __name__ == "__main__":
    with open("day08/input_example_1.txt") as test_input:
        input_string = test_input.read()

    moves, network = parse_input(input_string)
    count_steps_to_end(moves, network) == 2

    with open("day08/input_example_2.txt") as test_input:
        input_string = test_input.read()

    moves, network = parse_input(input_string)
    count_steps_to_end(moves, network) == 6

    with open("day08/input.txt") as test_input:
        input_string = test_input.read()

    moves, network = parse_input(input_string)
    print(count_steps_to_end(moves, network))
