from functools import cmp_to_key, partial, wraps

import nose

from integrationtest.decorators import dependable


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
        return int(a_depends_on_b) - int(b_depends_on_a)

    def loadTestsFromTestCase(self, testcase):
        suite = super().loadTestsFromTestCase(testcase)

        def make_dependable(tc_test):
            method = getattr(tc_test.test, tc_test.test._testMethodName)

            @dependable
            @wraps(method)
            def dependable_method(_, *a, **kw):
                return method(*a, **kw)

            setattr(
                tc_test.test.__class__,
                tc_test.test._testMethodName,
                dependable_method
            )
            return tc_test

        suite._tests = sorted(
            [make_dependable(test) for test in suite._tests],
            key=cmp_to_key(partial(self.test_cmp, testcase))
        )
        return suite
