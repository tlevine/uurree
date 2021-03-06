import os, signal, logging

from more_itertools import ilen, consume
import pytest

from .. import stratified_sample

logging.basicConfig(level = logging.DEBUG)
fn = os.path.abspath(os.path.join(__file__, '..', 'fixtures', 'parsing-pdfs.md'))

@pytest.mark.randomize(min_num = -10, max_num = 100, ncalls = 10)
def test_stratified(n:int, replace:bool):
    with open(fn, 'rb') as fp:
        # The function should finish quickly.
        def abort(*args):
            raise AssertionError('The function shouldn\'t take this long.')
        signal.signal(signal.SIGALRM, abort)
        signal.alarm(1)

        # We should get the right number of results.
        if n >= 0:
            observed = ilen(stratified_sample.sample(n, fp, replace = replace, give_up_at = 100))
            assert observed == n
        else:
            with pytest.raises(ValueError):
                consume(stratified_sample.sample(n, fp))

        signal.alarm(0)
