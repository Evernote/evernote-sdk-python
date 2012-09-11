import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='evernote',
    version='1.22',
    author='Evernote Corporation',
    author_email='en-support@evernote.com',
    url='http://dev.evernote.com',
    description='Evernote SDK for Python',
    long_description=read('README.md'),
    packages=find_packages('lib'),
    package_dir={'': 'lib'},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries',
    ],
    license='BSD',
)
