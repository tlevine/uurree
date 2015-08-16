import os, signal

import pytest

from .. import uurree

fn = os.path.abspath(os.path.join(__file__, '..', 'fixtures', 'parsing-pdfs.md'))

@pytest.mark.randomize(min_num = -10, max_num = 15382 * 2, ncalls = 10)
def test_simple_random(n:int):
    with open(fn) as fp:
        uurree.simple_random(n, fp, replace = True, give_up_at = 100)

@pytest.mark.skip
@pytest.mark.randomize(min_num = -10, max_num = 15382 * 2, ncalls = 10)
def test_find_line_start(seed:int, interval:int):
    with open(fn) as fp:
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

        # Unless we are at the beginning of the file, the character before
        # the present line should be a newline.
        if line_start > 0:
            fp.seek(line_start - 1)
            assert fp.read(1) == '\n'
        
        # We should not count the last line of the file.
        if fp.readline().endswith('\n'):
            line_end = fp.tell()
        else:
            line_end = fp.tell() + 1

        file_end = fp.seek(0, 2)

    assert line_start <= seed < line_end, (line_start, seed, line_end)
    if prev_char == '\n':
        assert line_start == seed
