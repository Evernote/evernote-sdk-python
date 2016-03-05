import os
from setuptools import setup, find_packages

constants = open('lib/evernote/edam/userstore/constants.py').read().split("\n")
for x in [x for x in constants if x.startswith('EDAM_VERSION')]:
    exec x


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='evernote',
    version="%i.%i.0" % (EDAM_VERSION_MAJOR, EDAM_VERSION_MINOR),
    author='Evernote Corporation',
    author_email='api@evernote.com',
    url='http://dev.evernote.com',
    description='Evernote SDK for Python',
    long_description=read('README.md'),
    packages=find_packages('lib'),
    packages=find_packages('lib',exclude=["*.thrift", "*.thrift.*", "thrift.*", "thrift"]),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries',
    ],
    license='BSD',
    install_requires=[
        'thrift',
        'oauth2',
    ],
)
