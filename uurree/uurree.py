from itertools import count, repeat
from random import randint

def simple_random(n, fp, replace = True, give_up_at = 100):
    '''
    If data are appended to the file during the function call,
    the appended data are ignored for the sampling.
    '''
    file_start = 0
    fp.seek(0, 2)
    file_end = fp.tell()
    emitted = set()
    for i in count():

        fp.seek(randint(file_start, file_end))
        line_start = find_line_start(fp)

        if replace and line_start not in emitted:
            emitted.add(line_start)
            yield fp.readline()

        if i > give_up_at and len(emitted) < (i / give_up_at):
            raise EnvironmentError('This file contains few line breaks, if any.')

    simple_random(args.n, fp)

def find_line_start(fp, interval = None):
    file_start = 0
    seed = fp.tell()

    fp.seek(0, 2)
    file_end = fp.tell()
    seed = min(seed, fp.tell())

    if not interval:
        interval = max(1, len(fp.readline()))

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
