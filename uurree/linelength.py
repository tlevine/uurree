import logging
from collections import Counter
from random import randint
from itertools import count

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
    for i in count():

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
        cdf[i] = total / n
    return cdf
