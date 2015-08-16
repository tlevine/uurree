from itertools import count, groupby
from random import randint

from more_itertools import ilen

from .uurree import find_line_start

def total(lines, filesize):
    '''
    Levy & Lemeshow, page 30
    Lohr, page 39, 219
    '''
    for i, the_lines in groupby(map(len, lines)):
        weight = filesize / i
        t_i = i * ilen(the_lines)
        t_w = t_i * weight

    sum(map(len, lines))
    expected_value = 0
    variance = 0
    for line in lines:
    #   inclusion_probability = len(line) / filesize
        sampling_weight = filesize / len(line)
        expected_value += weight * len(line)

    return {
        'weight': len(line) ** -1,
        'x': len(line),
    }

def sample(n, fp, replace = True, give_up_at = 100):
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

