#!/usr/bin/env python3

import subprocess

from tests import (TestAllFail, TestCircularDependency, TestDependencyFail,
                   TestPassInOrder)

testcases = [
    TestAllFail,
    TestCircularDependency,
    TestDependencyFail,
    TestPassInOrder
]

if __name__ == '__main__':
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
