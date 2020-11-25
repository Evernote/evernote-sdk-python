Evernote2 -- another Evernote SDK for Python
============================================

## Why Evernote2?


the official evernote sdk for python is not that good.


## Quick Start

#### Install

```bash
pip install evernote2
```


#### SDK API usage

example code: [evernote2/sample](evernote2/sample)


## Command Line Tools


#### Backup ALL notes

first,  a *TEMP* Developer Token from [https://app.yinxiang.com/api/DeveloperToken.action](https://app.yinxiang.com/api/DeveloperToken.action)]

then, run

```bash
python -m evernote2.tools.export_notes --china --token=<your-token>
```
