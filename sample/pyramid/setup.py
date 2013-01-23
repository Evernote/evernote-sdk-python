import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'waitress',
    'oauth2',
    'evernote'
    ]

setup(name='evernote_oauth_sample',
      version='0.0',
      description='evernote_oauth_sample',
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="evernote_oauth_sample",
      entry_points="""\
      [paste.app_factory]
      main = evernote_oauth_sample:main
      """,
      )
