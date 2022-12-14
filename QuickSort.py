import random


def quick_sort(seq):
    if len(seq) <= 1:
        return seq
    else:
        elem = seq[0]
        left = list(filter(lambda x: x < elem, seq))
        center = [i for i in seq if i == elem]
        right = list(filter(lambda x: x > elem, seq))

        return quick_sort(left) + center + quick_sort(right)


if __name__ == "__main__":
    sequence, n = [], 10
    for i in range(n):
        sequence.append(random.randint(-100, 100))
    sequence = quick_sort(sequence)
    print(sequence)