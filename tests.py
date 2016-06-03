import sys
import unittest

from integrationtest import TestCase, runner
from integrationtest.decorators import depends_on


if __name__ == '__main__':
    runner.run(*sys.argv)


class TestAllFail(TestCase):
    expect = 'FFF'

    def test_a(self):
        self.fail('We expect this to fail')

    def test_c(self):
        self.fail('We expect this to fail')

    def test_b(self):
        self.fail('We expect this to fail')


class TestCircularDependency(TestCase):
    expect = 'E'

    @depends_on('test_b')
    def test_a(self):
        pass

    @depends_on('test_a')
    def test_b(self):
        pass


class TestDependencyFail(TestCase):
    expect = 'F.S'

    def test_b(self):
        self.fail('We expect this to fail')

    @depends_on('test_b', 'test_c')
    def test_a(self):
        pass

    def test_c(self):
        pass


class TestPassInOrder(TestCase):
    expect = '...'

    @depends_on('test_b', 'test_c')
    def test_a(self):
        pass

    def test_c(self):
        pass

    def test_b(self):
        pass


class TestSetUpSkippedOnDependFail(TestCase):
    expect = 'FS'

    def setUp(self):
        if self._testMethodName == 'test_a':
            self.fail('We expect this to be unreachable')

    @depends_on('test_b')
    def test_a(self):
        pass

    def test_b(self):
        self.fail('We expect this to fail')
