import logging

logger = logging.getLogger(__name__)

def find_line_start(fp, interval = None):
    file_start = 0
    default_interval = 128

    seed = fp.tell()
    if seed == file_start:
        return file_start

    fp.seek(0, 2)
    file_end = fp.tell()
    seed = min(seed, fp.tell())

    if not interval:
        fp.readline()
        interval = len(fp.readline())
        if interval == 0:
            interval = default_interval
        interval = min(seed, interval)

    logger.debug('Seed: %d, Interval: %d' % (seed, interval))
    while True:
        fp.seek(seed - interval)
        text_in_interval = fp.read(interval)
        newlines = text_in_interval.count(b'\n')
        if newlines == 0:
            if seed - interval <= file_start:
                return file_start
            interval = min(seed, interval * 2)
        elif newlines == 1:
            fp.seek(seed - interval)
            fp.readline()
            return fp.tell()
        else:
            return seed - text_in_interval[::-1].index(b'\n')
