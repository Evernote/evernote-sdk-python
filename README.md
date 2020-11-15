Evernote SDK for Python
============================================

## Why this fork?

1. there are 2 versions of official evernote sdk for python, neither works well for python3

    - https://github.com/evernote/evernote-sdk-python3: Evernote API version 1.25. declared "This is a test SDK!"
    - https://github.com/evernote/evernote-sdk-python: Evernote API version 1.28. python2 only

2. no requirements.txt and not released to pypi officially.
3. the example code and docs on dev.evernote.com / dev.yinxiang.com are out of date


the python2 sdk is version 1.28, seems higher than python3(1.2.5).

Goal:

1. evernote SDK for Python3
2. good example code
3. release to pypi


## Plans


#### version 1.0.0 - Work In Progress

- [ ] API: list notebooks
- [ ] API: get note metadata
- [ ] API: get note content

#### version 0.0.1 - env and workflow setup

- [x] import evernote module and run hello world
- [x] unittest workflow
- [x] test coverage
- [x] workflow of release to pypi
- [x] add requirements.txt
