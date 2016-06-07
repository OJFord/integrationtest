import sys
import unittest

from integrationtest import TestCase, runner
from integrationtest.decorators import depends_on


if __name__ == '__main__':
    runner.run(*sys.argv)


class TestAllFailWithoutDependency(TestCase):
    expect = 'FFF'

    def test_a(self):
        self.fail('We expect this to fail')

    def test_c(self):
        self.fail('We expect this to fail')

    def test_b(self):
        self.fail('We expect this to fail')


class TestChainedDependantSkipsAfterFail(TestCase):
    expect = 'FSS'

    def test_a(self):
        self.fail('We expect this to fail')

    @depends_on('test_a')
    def test_b(self):
        pass

    @depends_on('test_b')
    def test_c(self):
        pass


class TestCircularDependency(TestCase):
    expect = 'E'

    @depends_on('test_b')
    def test_a(self):
        pass

    @depends_on('test_a')
    def test_b(self):
        pass


class TestDependencyFail(TestCase):
    expect = '[F\.]{2}S'

    def test_b(self):
        self.fail('We expect this to fail')

    @depends_on('test_b', 'test_c')
    def test_a(self):
        pass

    def test_c(self):
        pass


class TestRunInOrder(TestCase):
    expect = '\.{3}'
    _b_ran = False
    _c_ran = False

    @depends_on('test_b', 'test_c')
    def test_a(self):
        if not self.__class__._b_ran or not self.__class__._c_ran:
            self.fail('This test ran before its dependencies')

    def test_c(self):
        self.__class__._c_ran = True

    def test_b(self):
        self.__class__._b_ran = True


class TestSetUpSkippedOnDependFail(TestCase):
    expect = 'FS'

    def setUp(self):
        if self._testMethodName == 'test_a':
            self.fail('setUp ran for a test with failing dependency')

    @depends_on('test_b')
    def test_a(self):
        pass

    def test_b(self):
        self.fail('We expect this to fail')
