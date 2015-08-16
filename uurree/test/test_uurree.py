import os

import pytest

from .. import uurree

find_line_start_testcases = [
    (88, 0), (143, 0), (0, 0), (1321231, 0),
]

@pytest.mark.parametrize('seed, line_start', find_line_start_testcases)
def test_find_line_start(seed, line_start):
    fn = os.path.abspath(os.path.join(__file__, '..', 'fixtures', 'parsing-pdfs.md'))
    with open(fn) as fp:
        fp.seek(seed)
        observed = uurree.find_line_start(fp)
    assert observed == line_start
    
