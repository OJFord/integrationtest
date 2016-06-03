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
        proc = subprocess.run(
            ['python', 'tests.py', 'tests.py:{}'.format(case.__name__)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        assert proc.stdout.decode('utf-8').split('\n')[0] == case.expect
