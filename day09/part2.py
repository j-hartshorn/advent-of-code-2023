import numpy as np
from scipy.special import factorial


def parse_input(input_string: str) -> list[list[int]]:
    return np.array(
        [[int(num) for num in line.split()] for line in input_string.splitlines()]
    )


def orders(sequence):
    while not np.all(sequence == 0):
        yield sequence[0]
        sequence = np.diff(sequence)


def generate_term(power):
    def term(n):
        if power == 0:
            return 1
        elif power == 1:
            return n
        else:
            return (1 / factorial(power)) * np.prod(np.arange(n - power + 1, n + 1))

    return term


def generate_polynomial(orders):
    orders = list(orders)

    def polynomial(n):
        return sum(
            order * generate_term(power)(n) for power, order in enumerate(orders)
        )

    return polynomial


def get_next_number(sequence):
    polynomial = generate_polynomial(orders(sequence))
    generated_sequence = np.array(
        [np.around(polynomial(n)) for n in range(0, len(sequence) + 1)]
    )
    assert np.all(
        sequence == generated_sequence[:-1]
    ), f"Generated sequence \n{generated_sequence} does not match input sequence \n{sequence}"
    return int(generated_sequence[-1])


if __name__ == "__main__":
    with open("day09/input_example.txt") as f:
        input_string = f.read()

    sequences = parse_input(input_string)
    sequences = [list(reversed(seq)) for seq in sequences]
    next_values = [get_next_number(seq) for seq in sequences]
    assert next_values == [-3, 0, 5]
    assert sum(next_values) == 2

    with open("day09/input.txt") as f:
        input_string = f.read()

    sequences = parse_input(input_string)
    sequences = [list(reversed(seq)) for seq in sequences]
    next_values = [get_next_number(seq) for seq in sequences]
    print(sum(next_values))
