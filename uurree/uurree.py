import logging

logger = logging.getLogger(__name__)

def find_line_start(fp, interval = None):
    file_start = 0
    default_interval_coefficient = 3

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
        interval = min(seed, fp.readline() * default_interval_coefficient)

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
