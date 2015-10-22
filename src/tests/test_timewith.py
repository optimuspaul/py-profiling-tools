import time
import unittest
import uuid

from themis.timewith import timewith
from tests import influx


class TestTimewith(unittest.TestCase):

    run_id = uuid.uuid4()

    def test_simple_case(self):
        """Tests that a basic with timewith(...) works
        
        Expects to find a single point in the DB with a value ~1200
        """
        tag = "test.timewith.{0}.simple".format(self.run_id)
        with timewith(tag):
            time.sleep(1.2)
        results = influx.query("SELECT sum(value) FROM \"{0}\" WHERE time > now() - 1m".format(tag), database="themis_tests")
        points = list(results.get_points())
        self.assertEqual(len(points), 1)
        self.assertGreater(points[0]["sum"], 1200)
        # clean up the measurement we just made
        influx.query("DROP MEASUREMENT \"{0}\"".format(tag), database="themis_tests")

    def test_pointed_case(self):
        """Tests that timewith(...) with checkpoints works

        Expects to find 3 points in the db.
        """
        tag = "test.timewith.{0}.times".format(self.run_id)
        with timewith(tag) as instrum:
            time.sleep(0.1)
            instrum.checkpoint("hi-paul-1")
            time.sleep(1.2)
            instrum.checkpoint("hi-paul-2")
            time.sleep(0.1)
        results = influx.query("SELECT * FROM \"{0}\" WHERE time > now() - 1m".format(tag), database="themis_tests")
        points = list(results.get_points())
        self.assertEqual(len(points), 3)
        # clean up the measurement we just made
        influx.query("DROP MEASUREMENT \"{0}\"".format(tag), database="themis_tests")

    def test_inception_case(self):
        """Tests that timewith(...) with a child works

        Expects to find 2 points in the db for each timewith(...)
        """
        tag = "test.timewith.{0}.inception".format(self.run_id)
        with timewith(tag) as instrum:
            time.sleep(0.1)
            instrum.checkpoint("hi-paul-1")
            with timewith("purple", parent=instrum) as instrum2:
                time.sleep(1.2)
                instrum2.checkpoint("hi-paul-2")
                time.sleep(0.1)
        results = influx.query("SELECT elapsed, value FROM \"{0}\" WHERE time > now() - 1m".format(tag), database="themis_tests")
        points = list(results.get_points())
        self.assertEqual(len(points), 2)
        results = influx.query("SELECT elapsed, value, parent_elapsed, parent_since_checkpoint, parent_checkpoint FROM \"{0}.purple\" WHERE time > now() - 1m".format(tag), database="themis_tests")
        points = list(results.get_points())
        self.assertEqual(len(points), 2)
        # clean up the measurement we just made
        influx.query("DROP MEASUREMENT \"{0}\"".format(tag), database="themis_tests")
        influx.query("DROP MEASUREMENT \"{0}.purple\"".format(tag), database="themis_tests")

    def test_tagged_instrument(self):
        """Tests that timewith(...) with tags works

        Expects to find 1 point in the db tagged with specific tags
        """
        tag = "test.timewith.{0}.tagged".format(self.run_id)
        with timewith(tag, ts_tags={"cpu": 1, "cat": "loki"}):
            time.sleep(1.2)
        results = influx.query("SELECT * FROM \"{0}\" WHERE time > now() - 1m".format(tag), database="themis_tests")
        points = list(results.get_points())
        self.assertEqual(len(points), 1)
        self.assertEqual(points[0]["cpu"], "1")
        self.assertEqual(points[0]["cat"], "loki")
        # clean up the measurement we just made
        influx.query("DROP MEASUREMENT \"{0}\"".format(tag), database="themis_tests")
