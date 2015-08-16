from itertools import count, repeat
from random import randint

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
        fp.seek(randint(file_start, file_end))
        fp.readline()
        line = fp.readline()
        if len(line) > 0 and line[-1] == '\n':
            yield line
            lines_emitted += 1

        if lines_emitted == n:
            break
        if lines_emitted == 0 and i > 1000:
            raise EnvironmentError('It appears that this file contains no line breaks.')




    simple_random(args.n, fp)


