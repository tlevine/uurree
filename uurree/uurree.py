from itertools import count, repeat
from random import randint
import logging

logger = logging.getLogger(__name__)

def simple_random(n, fp, replace = True, give_up_at = 100):
    '''
    If data are appended to the file during the function call,
    the appended data are ignored for the sampling.
    '''
    if n < 0:
        raise ValueError('Sample size must be greater than zero.')

    file_start = 0
    fp.seek(0, 2)
    file_end = fp.tell()
    if replace:
        emitted = list()
    else:
        emitted = set()

    for i in count():

        fp.seek(randint(file_start, file_end))
        line_start = find_line_start(fp)

        if replace:
            emitted.append(line_start)
            yield fp.readline()
        elif line_start not in emitted:
            emitted.add(line_start)
            yield fp.readline()

        if len(emitted) == n:
            break
        elif i > give_up_at and len(emitted) < (i / give_up_at):
            raise EnvironmentError('This file probably doesn\'t have enough lines.')

def find_line_start(fp, interval = None):
    file_start = 0
    default_interval = 10

    seed = fp.tell()

    fp.seek(0, 2)
    file_end = fp.tell()
    seed = min(seed, fp.tell())

    if not interval:
        interval = max(1, min(seed, len(fp.readline())))

    logger.debug('Seed: %d, Interval: %d' % (seed, interval))
    while True:
        fp.seek(seed - interval)
        text_in_interval = fp.read(interval)
        newlines = text_in_interval.count('\n')
        if newlines == 0:
            if seed - interval <= file_start:
                return file_start
            interval = min(seed, interval * 2)
        elif newlines == 1:
            fp.seek(seed - interval)
            fp.readline()
            return fp.tell()
        else:
            return seed - text_in_interval[::-1].index('\n')
