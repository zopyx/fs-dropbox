from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys

tests_require = [
    'pytest',
    'pytest-cache',
    'pytest-cov',
]

install_requires = [
    'fs',
    'dropbox',
]


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name="pyfs-dropbox",
    version="0.3.3",
    description='A PyFilesystem backend for the Dropbox API.',
    long_description=open('README.rst').read(),
    author='Lukas Martinelli, Ben Timby',
    author_email='me@lukasmartinelli.ch, btimby@gmail.com',
    maintainer='Lukas Martinelli',
    maintainer_email='me@lukasmartinelli.ch',
    url='https://github.com/lukasmartinelli/fs-dropbox',
    license='GPLv3',
    install_requires=install_requires,
    extras_require={
        'test': tests_require
    },
    tests_require=tests_require,
    cmdclass={'test': PyTest},
    py_modules=['dropboxfs'],
    package_data={'': ['README.rst']},
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
)
