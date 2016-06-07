from functools import cmp_to_key, partial, wraps
from random import getrandbits

import nose

from integrationtest.decorators import try_or_add_failure


class DependencyLoader(nose.loader.TestLoader):
    class CircularDependency(Exception):
        pass

    def test_cmp(self, testcase, a, b):
        a_depends_on_b = (
            b.test._testMethodName in getattr(
                getattr(testcase, a.test._testMethodName),
                'dependencies',
                set()
            )
        )
        b_depends_on_a = (
            a.test._testMethodName in getattr(
                getattr(testcase, b.test._testMethodName),
                'dependencies',
                set()
            )
        )

        if a_depends_on_b and b_depends_on_a:
            raise self.CircularDependency(
                '{} and {} depend on each other!'.format(
                    a.test._testMethodName,
                    b.test._testMethodName
                )
            )
        elif a_depends_on_b:
            return 1
        elif b_depends_on_a:
            return -1
        else:  # shake out bugs from accidental dependency specs based on alpha
            return getrandbits(1)

    def loadTestsFromTestCase(self, testcase):
        suite = super().loadTestsFromTestCase(testcase)

        def make_dependable(tc_test):
            set_up = getattr(tc_test, 'setUp')
            method = getattr(tc_test.test, tc_test.test._testMethodName)

            @try_or_add_failure(method.__name__)
            @wraps(set_up)
            def dependable_set_up(_, *a, **kw):
                return set_up(*a, **kw)

            @try_or_add_failure()
            @wraps(method)
            def dependable_method(_, *a, **kw):
                return method(*a, **kw)

            setattr(
                tc_test.test.__class__,
                set_up.__name__,
                dependable_set_up
            )
            setattr(
                tc_test.test.__class__,
                method.__name__,
                dependable_method
            )
            return tc_test

        suite._tests = sorted(
            [make_dependable(test) for test in suite._tests],
            key=cmp_to_key(partial(self.test_cmp, testcase))
        )
        return suite
