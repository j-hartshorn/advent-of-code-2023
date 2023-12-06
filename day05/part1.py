from functools import cached_property
from typing import Self
from pydantic import BaseModel

from toolz import dicttoolz


def get_map_directions(map_name_line: str) -> tuple[str, str]:
    map_direction_string, _ = map_name_line.split(" ")
    map_from, _, map_to = map_direction_string.split("-")
    return map_from, map_to


class PartialMap(BaseModel):
    source_start_number: int
    destination_start_number: int
    length: int

    @cached_property
    def shift(self) -> int:
        return self.destination_start_number - self.source_start_number

    def will_map(self, input: int) -> bool:
        return (
            self.source_start_number <= input < self.source_start_number + self.length
        )

    def __call__(self, input: int) -> int:
        if self.will_map(input):
            map_result = input + self.shift
            return map_result
        else:
            return input

    @classmethod
    def from_string(cls, map_line: str) -> Self:
        destination_start_number, source_start_number, length = map_line.split(" ")
        source_start_number = int(source_start_number)
        destination_start_number = int(destination_start_number)
        length = int(length)
        return cls(
            source_start_number=source_start_number,
            destination_start_number=destination_start_number,
            length=length,
        )


class Map(BaseModel):
    source: str
    destination: str
    partial_mappings: list[PartialMap]

    def __call__(self, input: int) -> int:
        for mapping in self.partial_mappings:
            if mapping.will_map(input):
                input = mapping(input)
                break
        return input

    @classmethod
    def from_string(cls, map_chunk: str) -> Self:
        map_lines = map_chunk.split("\n")

        map_name_line = map_lines.pop(0)
        map_from, map_to = get_map_directions(map_name_line)

        map_lines = filter(lambda l: len(l) > 0, map_lines)
        mappings = list(map(PartialMap.from_string, map_lines))
        return cls(source=map_from, destination=map_to, partial_mappings=mappings)


class SeedMap(BaseModel):
    mappings: dict[str, Map]

    def __call__(self, input: int) -> int:
        mapping = self.mappings["seed"]
        map_to = mapping.destination
        input = mapping(input)
        while map_to in self.mappings:
            mapping = self.mappings[map_to]
            map_to = mapping.destination
            input = mapping(input)
        assert map_to == "location"
        return input

    @classmethod
    def from_string(cls, input_string: str) -> Self:
        # split chunks
        input_chunks = input_string.split("\n\n")
        input_chunks = input_chunks[1:]  # drop seeds chunk

        # Construct mapping
        mappings = {map.source: map for map in map(Map.from_string, input_chunks)}
        return cls(mappings=mappings)


def get_seed_numbers(input_string: str) -> list[int]:
    seed_line = input_string.split("\n\n")[0]
    return [int(d) for d in seed_line.split(":")[1].split(" ") if len(d) > 0]


def find_minimum_seed_location(input_string: str) -> int:
    seeds = get_seed_numbers(input_string)
    seed_map = SeedMap.from_string(input_string)
    seed_locations = list(map(seed_map, seeds))
    return min(seed_locations)


if __name__ == "__main__":
    with open("day05/input_example.txt") as test_input:
        input_string = test_input.read()

    assert find_minimum_seed_location(input_string) == 35

    with open("day05/input.txt") as test_input:
        input_string = test_input.read()

    print(find_minimum_seed_location(input_string))
