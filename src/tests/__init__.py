import logging
import os

from themis.log import TimeSeriesDataLogHandler


INFLUX_HOST = os.environ.get("INFLUX_HOST", "10.42.6.66")
INFLUX_PORT = os.environ.get("INFLUX_PORT", 8086)
INFLUX_USER = os.environ.get("INFLUX_USER", None)
INFLUX_PASS = os.environ.get("INFLUX_PASS", None)
INFLUX_DB = os.environ.get("INFLUX_DB", "themis_tests")

ts_handler = TimeSeriesDataLogHandler(INFLUX_HOST, INFLUX_PORT, INFLUX_USER, INFLUX_PASS, INFLUX_DB)

log = logging.getLogger()
log.addHandler(ts_handler)
log.setLevel(logging.DEBUG)
