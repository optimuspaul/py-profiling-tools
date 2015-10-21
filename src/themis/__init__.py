import time
import unittest
import yaml

from byzantine.engine.execute.constantinople import Emperor


class timewith():
    def __init__(self, name=''):
        self.name = name
        self.start = time.time()

    @property
    def elapsed(self):
        return time.time() - self.start

    def checkpoint(self, name=''):
        print('{timer} {checkpoint} took {elapsed} ms'.format(
            timer=self.name,
            checkpoint=name,
            elapsed=(self.elapsed * 1000.0),
        ).strip())

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.checkpoint('finished')
        pass


import cProfile


def do_cprofile(func):
    def profiled_func(*args, **kwargs):
        profile = cProfile.Profile()
        try:
            profile.enable()
            result = func(*args, **kwargs)
            profile.disable()
            return result
        finally:
            profile.print_stats(sort=True)
    return profiled_func


class TestTheBusThatCouldntSlowDown(unittest.TestCase):

    @do_cprofile
    def _apply_rule(self, context, rule, should_pass=True):
        with timewith("execute_rules"):
            report = Emperor.execute_rules(context, [rule])
            self.assertEqual(report['pass'], should_pass)
        return report.get('data')

    def test_simple_when(self):

        rule = {
            'name': 'testrule',
            'when': 'doc.amount == 1',
            'hide': [
                'doc.currency.dollar',
                'doc.amount',
            ]
        }
        context = {
            'currency': {
                'dollar': 100,
            },
            'amount': 1,
        }
        result = self._apply_rule(context, rule, should_pass=True)
        result = self._apply_rule(context, rule, should_pass=True)
        result = self._apply_rule(context, rule, should_pass=True)
