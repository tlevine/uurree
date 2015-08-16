import argparse, sys, os

from . import stratified_sample

argparser = argparse.ArgumentParser('Estimate how many lines are in a file.')
argparser.add_argument('file', type = argparse.FileType('rb'))
argparser.add_argument('--sample-size', '-n', type = int, default = 100, dest = 'n',
                       help = 'Number of lines to sample for the estimate')
argparser.add_argument('--confidence', '-c', type = int, default = .99,
                       help = 'Confidence level')
argparser.add_argument('--replace', '-r', action = 'store_true',
                       help = 'Sample with replacement?')


def main():
    args = argparser.parse_args()
    if args.n < 1:
        sys.stderr.write('Sample size must be at least one.\n')
        return 1
    elif not (0 < args.confidence < 1):
        sys.stderr.write('Confidence level must be between 0 and 1, exclusive.\n')
        return 1

    filesize = os.stat(args.file.name).st_size
    lines = stratified_sample.sample(args.n, args.file, replace = args.replace)
    stats = stratified_sample.total(filesize, lines)
    print(stats)

if __name__ == '__main__':
    main()
