import logging
import time


LOG = logging.getLogger(__name__)


class timewith():
    def __init__(self, name=''):
        self.name = name
        self.start = time.time()

    @property
    def elapsed(self):
        return time.time() - self.start

    def checkpoint(self, name=''):
        elapsed = (self.elapsed * 1000.0)
        LOG.debug('%s %s took %f ms', self.name, name, elapsed)
        return elapsed

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.checkpoint('finished')
        pass
