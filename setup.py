import os
import sys

from codecs import open

from setuptools import setup

from setuptools.command.test import test as TestCommand

here = os.path.abspath(os.path.dirname(__file__))


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        try:
            from multiprocessing import cpu_count
            self.pytest_args = ['-n', str(cpu_count()), '--boxed']
        except (ImportError, NotImplementedError):
            self.pytest_args = ['-n', '1', '--boxed']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


about = {}
with open(os.path.join(here, 'evernote2', '__version__.py'), 'r', 'utf-8') as f:
    exec(f.read(), about)

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


packages = ['evernote2']
requires = read('requirements.txt')
test_requirements = read('requirements-dev.txt')


setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=packages,
    package_data={'': ['LICENSE', 'NOTICE']},
    package_dir={'evernote2': 'evernote2'},
    include_package_data=True,
    # python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    install_requires=requires,
    license=about['__license__'],
    zip_safe=False,
    cmdclass={'test': PyTest},
    tests_require=test_requirements,
    extras_require={
        # 'security': ['pyOpenSSL >= 0.14', 'cryptography>=1.3.4'],
        # 'socks': ['PySocks>=1.5.6, !=1.5.7'],
    },
)
