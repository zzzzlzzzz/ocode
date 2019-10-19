from collections import Counter
from math import ceil
from argparse import ArgumentParser, Namespace


import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt


def generate(args: 'Namespace') -> None:
    """Generate data from arguments

    :param args: CL-arguments
    :return: None
    """
    np.savetxt(args.destination, (np.random.random([args.m, args.n]) * 2.0) - 1.0, delimiter=',')


def calculate(args) -> None:
    """Calculate results by arguments

    :param args: CL-arguments
    :return: None
    """
    min_distance, min_i, min_j = None, None, None
    max_distance, max_i, max_j = None, None, None
    hist = Counter()

    array = np.loadtxt(args.source, delimiter=',')
    for i, row_a in enumerate(array[: len(array) - 1]):
        for j, row_b in enumerate(array[i + 1:]):
            distance = np.linalg.norm(row_a - row_b)
            if min_distance is None or distance < min_distance:
                min_distance, min_i, min_j = distance, i, j
            if max_distance is None or distance > max_distance:
                max_distance, max_i, max_j = distance, i, j
            hist[ceil(distance * 10) / 10] += 1

    labels, values = zip(*sorted(hist.items(), key=lambda _: _[0]))

    plt.bar([_ for _ in range(len(values))], values, 1)
    plt.xticks([_ + 0.5 for _ in range(len(labels))], labels, rotation='vertical', fontsize='6')
    extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
    plt.legend([extra, ],
               ("MIN distance {} ({} v {})\nMAX distance {} ({} v {})".
                format(min_distance, min_i, min_j, max_distance, max_i, max_j), ))
    plt.savefig(args.destination)


def main() -> None:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()
    subparsers.required = True
    subparsers.metavar = 'ACTION'

    parser_generate = subparsers.add_parser('gen', help='Generate matrix')
    parser_generate.add_argument('destination', help='Destination file', metavar='DST')
    parser_generate.add_argument('m', type=int, help='Matrix rows', metavar='M')
    parser_generate.add_argument('n', type=int, help='Matrix cols', metavar='N')
    parser_generate.set_defaults(func=generate)

    parser_calculate = subparsers.add_parser('calc', help='Calculate matrix')
    parser_calculate.add_argument('source', help='Source file', metavar='SRC')
    parser_calculate.add_argument('destination', help='Destination image file (e.g. r.png)', metavar='DST')
    parser_calculate.set_defaults(func=calculate)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
