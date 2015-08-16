import logging

logger = logging.getLogger(__name__)

def find_line_start(fp, interval = None):
    file_start = 0

    # Ignore blank last lines.
    seed = fp.tell()
    if fp.readline() == b'':
        seed -= 1

    # Find the end of the file.
    fp.seek(0, 2)
    file_end = fp.tell()

    # Return 0 right away if we're at the beginning of the file.
    if seed <= file_start or file_end <= file_start:
        return file_start

    # Set the backwards scan interval
    if not interval:
        interval = min(seed, len(fp.readline()))

    logger.debug('Seed: %d, Interval: %d' % (seed, interval))
    fp.seek(seed - interval)

    offset = int(interval)
    while True:
        fp.seek(min(file_start, seed - offset))
        text_in_interval = fp.read(offset)
        newlines = text_in_interval.count(b'\n')
        if newlines == 0:
            if seed - offset <= file_start:
                return file_start
            assert False, offset
            offset += interval
        else:
            return seed - offset - text_in_interval[::-1].index(b'\n')
