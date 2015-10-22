import logging
import time
from datetime import datetime

from influxdb import InfluxDBClient


ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


class TimeSeriesDataLogHandler(logging.Handler):
    """
    A handler class which writes logging records to a time series database when
    apropriate extra data is supplied.
    """

    def __init__(self, influx_host=None, influx_port=8086, influx_user=None, influx_pass=None, influx_db="tslog"):
        """
        Initialize the handler.
        """
        super(TimeSeriesDataLogHandler, self).__init__()
        self.__influx = InfluxDBClient(influx_host, influx_port, influx_user, influx_pass, influx_db)

    def emit(self, record):
        if hasattr(record, "ts_data"):
            ts_data = getattr(record, "ts_data")
            ts_data.apply_log_info(record)
            self.__influx.write_points([ts_data.to_dict()])


class TSData(object):

    def __init__(self, measurement, fields, tags):
        self.measurement = measurement
        self.fields = fields or dict()
        self.tags = tags or dict()
        self.ts = time.time()

    def apply_log_info(self, record):
        self.fields["msg"] = getattr(record, "msg")
        if hasattr(record, "args"):
            self.fields["msg"] = self.fields["msg"] % getattr(record, "args")
        self.ts = getattr(record, "created")

    def to_dict(self):
        return {
            "measurement": self.measurement,
            "tags": self.tags,
            "fields": self.fields,
            "time": datetime.utcfromtimestamp(self.ts).strftime(ISO_FORMAT),
        }
