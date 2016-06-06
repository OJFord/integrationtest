import sys
from distutils.core import Command, setup
from subprocess import run


class RunTests(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        proc = run('./test/runner', shell=True)
        sys.exit(proc.returncode)

setup(
    name='integrationtest',
    version='0.2.4',
    author='Ollie Ford <me@ojford.com>',
    packages=['integrationtest'],
    long_description=open('README.md').read(),
    cmdclass={'test': RunTests}
)
