import logging
from collections import Counter
from random import randint, random
import itertools

from sliding_window import window
from more_itertools import ilen

logger = logging.getLogger(__name__)

def estimated_cdf(n, fp, give_up_at = 100):
    '''
    If data are appended to the file during the function call,
    the appended data are ignored for the sampling.

    Samples are with replacement.
    '''
    if n < 0:
        raise ValueError('Sample size must be greater than zero.')

    file_start = 0
    fp.seek(0, 2)
    file_end = fp.tell()

    negative_absolute_cdf = Counter()
    for i in itertools.count():

        # Select a random byte.
        fp.seek(randint(file_start, file_end))

        line = fp.readline()
        if line.endswith(b'\n'):
            negative_absolute_cdf[len(line)] += 1
            if sum(negative_absolute_cdf.values()) == n:
                break

        elif i > give_up_at and len(negative_absolute_cdf) < (i / give_up_at):
            raise EnvironmentError('This file probably doesn\'t have enough lines.')

    cdf = Counter()
    total = 0
    for i in sorted(negative_absolute_cdf):
        total += negative_absolute_cdf[i]
        cdf[i] = 1 - total / n
    return cdf

def exact_cdf(fp):
    '''
    what is this the cdf of?
    '''
    negative_absolute_cdf = Counter()
    n = 0

    for line in fp:
        for i in range(len(line)):
            negative_absolute_cdf[i] += 1
            n += 1

    cdf = Counter()
    total = 0
    for i in sorted(negative_absolute_cdf):
        total += negative_absolute_cdf[i]
        cdf[i] = total / n
    return cdf

def bin(cdf, n = 5, func = sum):
    binsize = (max(cdf) - min(cdf)) / n
    current_bin = 1
    x = Counter()
    for line_length in sorted(cdf):
        bin_key = min(cdf) + binsize * current_bin
        x[bin_key] = func([x[bin_key], cdf[line_length]])
        if line_length > bin_key:
            current_bin += 1
    return x

def derivative(counter):
    dcounter = Counter()
    for left, right in window(itertools.chain([min(counter) - 1], sorted(counter))):
        dcounter[right] = counter[right] - counter[left]
    return dcounter

def inverse_cdf(cdf, x):
    cum_freq = 0
    for i in sorted(cdf):
        cum_freq += cdf[i]
        if cum_freq > x:
            return i

def resample(cdf, total_length):
    '''
    Generate a distribution of line lengths with a particular total length.
    '''
    length = 0
    while length < total_length:
        r = random()
        for line_length in sorted(cdf):
            if cdf[line_length] > r:
                yield line_length
                length += line_length
                break

# bin(derivative(estimated_cdf(10, open('/Users/t/email.sh', 'rb'))), func = sum)
# bin(derivative(exact_cdf(open('/Users/t/email.sh', 'rb'))), func = sum)
# ilen(resample(exact_cdf(open('/Users/t/email.sh', 'rb')), 1000))
