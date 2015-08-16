from itertools import count, repeat
from random import randint

"""
def simple_random(n, fp):
    '''
    with replacement

    If data are appended to the file during the function call,
    the appended data are ignored for the sampling.
    '''
    file_start = fp.tell()
    fp.seek(0, 2)
    file_end = fp.tell()
    
    lines_emitted = 0
    for i in count():
        trial = randint(file_start, file_end)
        fp.seek(trial)
        rough_linelength_estimate = len(fp.readline()) * 2
        for j in count():
            fp.seek(trial - j * rough_linelength_estimate)
            precise_linelength_estimate = fp.readline()
            if fp.tell() < trial:






        if len(line) > 0 and line[-1] == '\n':
            yield line
            lines_emitted += 1

        if lines_emitted == n:
            break
        if lines_emitted == 0 and i > 1000:
            raise EnvironmentError('It appears that this file contains no line breaks.')




    simple_random(args.n, fp)
"""


def find_line_start(fp, interval = None):
    seed = fp.tell()
    fp.seek(0, 2)

    file_end = fp.tell()
    if seed > file_end:
        seed = file_end

    if not interval:
        interval = max(1, len(fp.readline()))
    elif interval > file_end:
        interval = file_end

    fp.seek(seed)

    while True:
        fp.seek(seed - interval)
        text_in_interval = fp.read(interval)
        newlines = text_in_interval.count('\n')
        if newlines == 0:
            interval = max(seed, interval * 2)
        elif newlines == 1:
            fp.seek(seed - interval)
            fp.readline()
            return fp.tell()
        else:
            return seed - text_in_interval[::-1].index('\n')
