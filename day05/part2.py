from functools import reduce
from typing import Generator

from pydantic import BaseModel


class Range(BaseModel):
    start: int
    end: int


class RangeMap(BaseModel):
    start: int
    end: int
    offset: int


def parse(
    input_string,
) -> (list[Range], list[list[RangeMap]]):
    chunks = input_string.split("\n\n")
    seed_chunk = chunks.pop(0)
    seeds = [int(d) for d in seed_chunk.split(":")[1].split(" ") if len(d) > 0]
    seed_ranges = [
        Range(start=seeds[i], end=seeds[i] + seeds[i + 1])
        for i in range(0, len(seeds), 2)
    ]

    mapping_stages = []
    for chunk in chunks:
        lines = chunk.splitlines()
        mappings = []
        for line in lines[1:]:
            if len(line) == 0:
                continue
            nums = [int(d) for d in line.split(" ") if len(d) > 0]
            mappings.append(
                RangeMap(start=nums[1], end=nums[1] + nums[2], offset=nums[0] - nums[1])
            )
        mapping_stages.append(mappings)

    return seed_ranges, mapping_stages


def remap(
    seed_ranges: list[Range], mappings: list[RangeMap]
) -> Generator[Range, None, None]:
    mappings = sorted(mappings, key=lambda m: m.start)
    for seed_range in seed_ranges:
        mapped_range_start = seed_range.start
        for mapping in mappings:
            mapped_range_end = mapping.end

            if (
                mapping.start >= seed_range.end
                or mapped_range_start >= mapped_range_end
            ):
                # No overlap
                continue
            if mapped_range_start < mapping.start:
                yield Range(start=mapped_range_start, end=mapping.start)
                mapped_range_start = mapping.start
            mapped_range_end = min(seed_range.end, mapped_range_end)
            yield Range(
                start=mapped_range_start + mapping.offset,
                end=mapped_range_end + mapping.offset,
            )
            mapped_range_start = mapped_range_end
        if mapped_range_start < seed_range.end:
            yield Range(start=mapped_range_start, end=seed_range.end)


def find_lowest_location_number(input_string: str) -> int:
    seed_ranges, mapping_stages = parse(input_string)
    location_ranges = list(reduce(remap, mapping_stages, seed_ranges))
    return min(r.start for r in location_ranges)


if __name__ == "__main__":
    with open("day05/input_example.txt") as input_file:
        input_string = input_file.read()

    assert find_lowest_location_number(input_string) == 46

    with open("day05/input.txt") as input_file:
        input_string = input_file.read()

    print(find_lowest_location_number(input_string))
