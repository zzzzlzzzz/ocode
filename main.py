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
    results = []
    array = np.loadtxt(args.source, delimiter=',')
    for i, row_a in enumerate(array[: len(array) - 1]):
        for j, row_b in enumerate(array[i + 1:]):
            results.append([i, j + i + 1, np.linalg.norm(row_a - row_b)])
    minimal = min(results, key=lambda _: _[2])
    maximal = max(results, key=lambda _: _[2])

    hist = Counter(ceil(_[2] * 10) / 10 for _ in results)
    labels, values = zip(*sorted(hist.items(), key=lambda _: _[0]))

    plt.bar([_ for _ in range(len(values))], values, 1)
    plt.xticks([_ + 0.5 for _ in range(len(labels))], labels, rotation='vertical', fontsize='6')
    extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
    plt.legend([extra, ],
               ("MIN distance {} ({} v {})\nMAX distance {} ({} v {})".
                format(minimal[2], minimal[0], minimal[1], maximal[2], maximal[0], maximal[1]), ))
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
