from functools import reduce
from math import lcm
import re


def parse_network(network_string: str):
    edge_pattern = re.compile(r"([A-Z0-9]{3}) = \(([A-Z0-9]{3}), ([A-Z0-9]{3})\)")
    network = {}
    for line in network_string.splitlines():
        start, left, right = edge_pattern.match(line).groups()
        network[start] = (left, right)
    return network


def parse_input(
    input_string: str,
):
    movement_string, network_string = input_string.split("\n\n")
    network = parse_network(network_string)
    return movement_string, network


def answer(input_string):
    movement_string, network = parse_input(input_string)
    starting_locations = [k for k in network if k[2] == "A"]

    # Each starting location takes the first step into a loop
    # We want to find that loop size
    loop_size = {}
    for starting_location in starting_locations:
        current_location = starting_location
        step_count = 0

        while current_location[2] != "Z":
            move = movement_string[step_count % len(movement_string)]
            move_idx = 0 if move == "L" else 1

            current_location = network[current_location][move_idx]
            step_count += 1

        loop_size[starting_location] = step_count

    # The answer then is the LCM of the loop sizes
    return lcm(*loop_size.values())


if __name__ == "__main__":
    with open("day08/input_example_3.txt") as test_input:
        input_string = test_input.read()

    assert answer(input_string) == 6

    with open("day08/input.txt") as f:
        input_string = f.read()

    print(answer(input_string))
