import os, signal, logging

import pytest

from .. import uurree

logging.basicConfig(level = logging.DEBUG)
fn = os.path.abspath(os.path.join(__file__, '..', 'fixtures', 'parsing-pdfs.md'))

@pytest.mark.randomize(min_num = -10, max_num = 15382 * 2, ncalls = 10)
def test_find_line_start(seed:int, interval:int):
    with open(fn, 'rb') as fp:
        fp.seek(0, 2)
        seed = min(seed, fp.tell())
        interval = min(interval, seed)

        fp.seek(seed - 1)
        prev_char = fp.read(1)

        # The function should finish quickly.
        def abort(*args):
            raise AssertionError('The function shouldn\'t take this long.')
        signal.signal(signal.SIGALRM, abort)
        signal.alarm(1)
        line_start = uurree.find_line_start(fp, interval = interval)
        signal.alarm(0)

        fp.seek(line_start)
        print('Line is %s.' % fp.readline())

        # Unless we are at the beginning of the file, the character before
        # the present line should be a newline.
        if line_start > 0:
            fp.seek(line_start - 1)
            assert fp.read(1) == b'\n'
        
        line_end = fp.tell()
        file_end = fp.seek(0, 2)

        # We should not count empty last lines.
        fp.seek(line_start)
        assert fp.readline() != b''
        
    assert line_start <= seed < line_end, (line_start, seed, line_end)
    if prev_char == '\n':
        assert line_start == seed
