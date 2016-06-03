import unittest
import nose
from integrationtest.loader import DependencyLoader

TestCase = unittest.TestCase


class Runner:
    def run(self, *a):
        return nose.main(
            testLoader=DependencyLoader,
            argv=list(a)
        )

runner = Runner()
