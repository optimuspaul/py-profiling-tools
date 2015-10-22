import logging
import unittest
import uuid

from themis.log import TSData
from tests import influx


class TestEmit(unittest.TestCase):

    def test_emit_001(self):
        logger = logging.getLogger(__name__)
        tag = uuid.uuid4()
        measurement = "test.themis.emit.{0}".format(tag)
        td = TSData(measurement, {"value": 1}, {"test": "TestEmit.test_emit_001", "test_id": tag})
        logger.debug("just me testing", extra={"ts_data": td})
        logger.error("is this an error?", extra={"ts_data": td})
        results = influx.query("SELECT sum(value) FROM \"themis_tests\".\"default\".\"{1}\" WHERE time > now() - 1m AND test_id = '{0}'".format(tag, measurement))
        points = list(results.get_points())
        self.assertEqual(len(points), 1)
        self.assertEqual(points[0]["sum"], 2)
        influx.query("DROP MEASUREMENT \"{0}\"".format(measurement), database="themis_tests")
