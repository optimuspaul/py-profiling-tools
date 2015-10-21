import logging
import unittest

from themis.log import TSData


class TestEmit(unittest.TestCase):

    def test_emit_001(self):
        logger = logging.getLogger(__name__)
        print("")
        td = TSData("test", {"value": 1}, {"test": "TestEmit.test_emit_001"})
        logger.debug("just me testing", extra={"ts_data": td})
        logger.error("is this an error?", extra={"ts_data": td})
        print("see anything?")
