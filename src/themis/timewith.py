import logging
import time

from themis.log import TSData


LOG = logging.getLogger(__name__)


class timewith():
    def __init__(self, measurement='events', parent=None, ts_tags=None):
        self.parent = parent
        self.measurement = measurement
        if parent:
            self.measurement = ".".join([self.parent.measurement, measurement])
        self.last_check = None
        self.last_checkpoint_name = None
        self.start = self.last_check = time.time()
        self.ts_tags = ts_tags

    @property
    def elapsed(self):
        return time.time() - self.start

    def checkpoint(self, name):
        self.last_checkpoint_name = name
        elapsed = (self.elapsed * 1000.0)
        now = time.time()
        interval_time = (now - self.last_check) * 1000.0
        self.last_check = now
        tags = {"checkpoint": name}
        fields = {"elapsed": elapsed, "value": interval_time}
        if self.ts_tags:
            for key in self.ts_tags:
                tags[key] = self.ts_tags[key]
        if self.parent:
            tags["parent"] = self.parent.measurement
            fields["parent_elapsed"] = self.parent.elapsed
            fields["parent_since_checkpoint"] = (now - self.parent.last_check) * 1000.0
            fields["parent_checkpoint"] = self.parent.last_checkpoint_name
        td = TSData(self.measurement, fields, tags)
        LOG.debug('%s %s took %f ms', self.measurement, name, elapsed, extra={"ts_data": td})
        return elapsed

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.checkpoint('finished')
