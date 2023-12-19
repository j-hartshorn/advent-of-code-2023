from collections import Counter
from enum import IntEnum
from functools import cached_property, total_ordering
from operator import itemgetter
from typing import Self

from pydantic import BaseModel, Field


class Card(IntEnum):
    joker = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10
    queen = 12
    king = 13
    ace = 14

    @classmethod
    def from_char(cls, c: str) -> Self:
        match c:
            case "2":
                return cls.two
            case "3":
                return cls.three
            case "4":
                return cls.four
            case "5":
                return cls.five
            case "6":
                return cls.six
            case "7":
                return cls.seven
            case "8":
                return cls.eight
            case "9":
                return cls.nine
            case "T":
                return cls.ten
            case "J":
                return cls.joker
            case "Q":
                return cls.queen
            case "K":
                return cls.king
            case "A":
                return cls.ace
            case _:
                raise ValueError(f"Invalid card: {c}")


class HandType(IntEnum):
    five_of_a_kind = 9
    four_of_a_kind = 8
    full_house = 7
    three_of_a_kind = 6
    two_pair = 5
    one_pair = 4
    high_card = 3


@total_ordering
class Hand(BaseModel):
    cards: list[Card] = Field(..., min_items=5, max_items=5)
    string: str

    @classmethod
    def from_string(cls, s: str) -> Self:
        cards = [Card.from_char(c) for c in s]
        return cls(cards=cards, string=s)

    @cached_property
    def type(self) -> HandType:
        card_counter = Counter(self.cards)

        # remove the joker count and add it to the most common card, breaking ties with card value
        joker_count = card_counter.pop(Card.joker, 0)
        if joker_count == 5:  # JJJJJ
            return HandType.five_of_a_kind

        # Get the most common card, breaking ties with card value
        highest_counted_card = sorted(
            card_counter.items(), key=itemgetter(1, 0), reverse=True
        )[0][0]
        card_counter[highest_counted_card] += joker_count

        if 5 in card_counter.values():
            return HandType.five_of_a_kind
        elif 4 in card_counter.values():
            return HandType.four_of_a_kind
        elif 3 in card_counter.values() and 2 in card_counter.values():
            return HandType.full_house
        elif 3 in card_counter.values():
            return HandType.three_of_a_kind
        elif len([v for v in card_counter.values() if v == 2]) == 2:
            return HandType.two_pair
        elif 2 in card_counter.values():
            return HandType.one_pair
        else:
            return HandType.high_card

    def card_showdown_gt(self, other: Self) -> bool:
        for self_card, other_card in zip(self.cards, other.cards):
            if self_card == other_card:
                continue
            else:
                return self_card > other_card
        raise ValueError("Hands are equal")

    def __eq__(self, other: Self) -> bool:
        return all(c1 == c2 for c1, c2 in zip(self.cards, other.cards))

    def __gt__(self, other: Self) -> bool:
        if not self.type == other.type:
            return self.type > other.type
        else:
            return self.card_showdown_gt(other)


@total_ordering
class Play(BaseModel):
    hand: Hand
    bid: int

    @classmethod
    def from_string(cls, s: str) -> Self:
        hand, bid = s.split(" ")
        return cls(hand=Hand.from_string(hand), bid=int(bid))

    def __eq__(self, other: Self) -> bool:
        return self.hand == other.hand

    def __gt__(self, other: Self) -> bool:
        return self.hand > other.hand


def total_winnings(plays: list[Play]) -> int:
    return sum(
        play.bid * (1 + rank_index) for rank_index, play in enumerate(sorted(plays))
    )


if __name__ == "__main__":
    with open("day07/input_example.txt") as test_input:
        input_string = test_input.read()

    plays = [Play.from_string(s) for s in input_string.splitlines()]
    assert total_winnings(plays) == 5905

    with open("day07/input.txt") as test_input:
        input_string = test_input.read()

    plays = [Play.from_string(s) for s in input_string.splitlines()]
    print(total_winnings(plays))
