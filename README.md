# integrationtest
![Travis CI build status](https://travis-ci.org/OJFord/integrationtest.svg?branch=master)

A simple wrapper around unittest to make it nicer to use for integration testing.

## Why not just use unittest?

In integration tests, it may make a lot of sense to:
- have tests that aren't quite 'setUp', but need to happen in order
- have tests that skip if another fails; they depend on its success

These features aren't in unittest, probably never will be, and shouldn't be.

## Installation

```sh
pip install integrationtest
```

## Usage

### Running
You can:
 - use an instance of `integrationtest.Runner`, such as `integrationtest.runner`, and call `Runner#run` with arguments as you would `nosetests` on the command line;
 - import `integrationtest.loader.DependencyLoader`, and use it with nose `run`/`main`/`TestProgram` as the keyword argument `testLoader`


### Dependent tests
```python
import sys

from integrationtest import runner
from integrationtest import TestCase
from integrationtest.decorators import depends_on


class TestCase(TestCase):
	test_b_happened = False
	test_c_happened = False

	def test_b(self):
		self.fail()
		self.__class__.test_b_happened = True

	@depends_on('test_b', 'test_c')
	def test_a(self):
		ok = self.__class__.test_b_happened and self.__class__.test_c_happened
		if not ok:
			raise Exception

	def test_c(self):
		self.__class__.test_c_happened = True


if __name__ == '__main__':
	runner.run(*sys.argv)
```

*Without* integrationtest, the methods would be alphanumerically sorted, and `test_a` would happen first, erring because it relies on an action performed by `test_b`; which hasn't yet happened:

> test_a ... ERROR  
> test_b ... FAIL  
> test_c ... ok  

*With* integrationtest, the dependency is picked up, and `test_a` is skipped after `test_b` fails:

> test_b ... FAIL  
> test_c ... ok  
> test_a ... SKIP: Because a dependency failed  
