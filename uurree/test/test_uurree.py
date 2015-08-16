import os

import pytest

from .. import uurree

find_line_start_testcases = [
    (88, 0), (143, 0), (0, 0), (1321231, 0),
]

@pytest.mark.randomize(min_num = -10, max_num = 15382 * 2)
@pytest.mark.parametrize('seed, expected_line_start', find_line_start_testcases)
def test_find_line_start(seed, expected_line_start, interval:int):
    fn = os.path.abspath(os.path.join(__file__, '..', 'fixtures', 'parsing-pdfs.md'))
    with open(fn) as fp:
        fp.seek(seed)
        line_start = uurree.find_line_start(fp, interval = interval)
        if line_start == 0:
            prev_char = '\n'
        else:
            fp.seek(line_start - 1)
            prev_char = fp.read(1)
        fp.readline()
        line_end = fp.tell()

    assert prev_char == '\n'
    assert line_start < seed < line_end
   #assert observed == expected_line_start
    
