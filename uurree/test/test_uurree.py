import os, signal

import pytest

from .. import uurree

@pytest.mark.randomize(min_num = -10, max_num = 15382 * 2)
def test_find_line_start(seed:int, interval:int):
    fn = os.path.abspath(os.path.join(__file__, '..', 'fixtures', 'parsing-pdfs.md'))
    with open(fn) as fp:
        fp.seek(seed - 1)
        prev_char = fp.read(1)


        def abort(*args):
            raise TimeoutError('The function shouldn\'t take this long.')
        signal.signal(signal.SIGALRM, abort)
        signal.alarm(1)
        line_start = uurree.find_line_start(fp, interval = interval)
        signal.alarm(0)

        if line_start > 0:
            fp.seek(line_start - 1)
            assert fp.read(1) == '\n'
        
        # We should not count the last line of the file.
        if fp.readline().endswith('\n'):
            line_end = fp.tell()
        else:
            line_end = fp.tell() + 1

        file_end = fp.seek(0, 2)

    # To make the assertions easier
    if seed >= file_end:
        seed = file_end
    assert line_start <= seed < line_end, (line_start, seed, line_end)
    if prev_char == '\n':
        assert line_start == seed
