import os

import pytest

from .. import uurree

@pytest.mark.randomize(min_num = -10, max_num = 15382 * 2)
def test_find_line_start(seed:int, interval:int):
    fn = os.path.abspath(os.path.join(__file__, '..', 'fixtures', 'parsing-pdfs.md'))
    with open(fn) as fp:
        fp.seek(seed)
        line_start = uurree.find_line_start(fp, interval = interval)
        if line_start == 0:
            prev_char = '\n'
        else:
            fp.seek(line_start - 1)
            prev_char = fp.read(1)
        
        # We should not count the last line of the file.
        if fp.readline().endswith('\n'):
            line_end = fp.tell()
        else:
            line_end = fp.tell() + 1

        file_end = fp.seek(0, 2)

    # To make the assertions easier
    if seed >= file_end:
        seed = file_end
    assert prev_char == '\n'
    assert line_start < seed < line_end
