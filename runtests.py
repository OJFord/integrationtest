#!/usr/bin/env python3

import subprocess
import sys

from tests import (
    TestAllFailWithoutDependency, TestCircularDependency, TestDependencyFail,
    TestRunInOrder, TestSetUpSkippedOnDependFail
)

testcases = [
    TestAllFailWithoutDependency,
    TestCircularDependency,
    TestDependencyFail,
    TestRunInOrder,
    TestSetUpSkippedOnDependFail
]

if __name__ == '__main__':
    failures = []
    for case in testcases:
        print(case.__name__ + ' ... ', end='')
        proc = subprocess.run(
            ['python', 'tests.py', 'tests.py:{}'.format(case.__name__)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        result = proc.stdout.decode('utf-8').split('\n')[0]
        try:
            assert result == case.expect
            print('ok')
        except:
            print('FAIL: got %s; expected %s' % (result, case.expect))
            failures.append((
                case.__name__,
                '{} != {}'.format(result, case.expect),
                proc.stdout
            ))
    for failure in failures:
        print('\n##########################################', file=sys.stderr)
        print('# {}: {}'.format(failure[0], failure[1]), file=sys.stderr)
        print('##########################################', file=sys.stderr)
        print(str(failure[2], 'utf-8'), file=sys.stderr)
    if failures:
        exit(1)
