import os

from .. import uurree

def test_find_line_start(seed, line_start):
    fn = os.path.abspath(os.path.join(__file__, '..', 'fixtures', 'parsing-pdfs.md'))
    with open(fn) as fp:
        fp.seek(seed)
        observed = uurree.find_line_start(fp)
    assert observed == line_start
    
