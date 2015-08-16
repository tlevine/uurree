import argparse, sys

from . import uurree

argparser = argparse.ArgumentParser('Estimate how many lines are in a file.')
argparser.add_argument('file', type = argparse.FileType('r'))
argparser.add_argument('--sample-size', '-n', type = int, default = 100, dest = 'n',
                       help = 'Number of lines to sample for the estimate')
argparser.add_argument('--confidence', '-c', type = int, default = .99, dest = 'n',
                       help = 'Confidence level')
argparser.add_argument('--replace', '-r', action = 'store_true'
                       help = 'Sample with replacement?')


def main():
    args = argparser.parse_args()
    if args.n < 1:
        sys.stderr.write('Sample size must be at least one.\n')
        return 1
    elif not (0 < args.confidence < 1):
        sys.stderr.write('Confidence level must be between 0 and 1, exclusive.\n')
        return 1

    lines = uurree.uurree(args.n, args.file, args.file, replace = args.replace)

    for line in lines:
        len(line)
    sum(map(len, lines))

if __name__ == '__main__':
    main()
