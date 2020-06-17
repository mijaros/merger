Merger
======

Tool for merging pull requests based on labels applied to them.

Installation
------------

Project can be now installed from github via pip:

```bash
pip install git+https://github.com/mijaros/merger
```

In order to protect your python package database we do recommend working 
in [Virtualenv](https://virtualenv.pypa.io/en/latest/).

```bash
virtualenv mergerenv
source mergerenv/bin/activate
pip install git+https://github.com/mijaros/merger
```

Usage
-----

To run merger you'll need two things in advance:

* Github api access token [here](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line).
* Configured `ssh-agent` which has write access to publish remote and read access to the project with pull requests.


