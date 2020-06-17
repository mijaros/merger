from setuptools import setup, find_packages
from os import path

# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="merger",
    version="0.0.1",
    description="Tool to build branch from all opened PRs with applied label",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mijaros/merger",
    author="Miroslav Jaroš",
    author_email="mirek@mijaros.cz",
    keywords="github git merging",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    python_requires=">=3.6, <4",
    install_requires=[
        "certifi==2020.4.5.2",
        "chardet==3.0.4",
        "coloredlogs==14.0",
        "deprecated==1.2.10; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "gitdb==4.0.5; python_version >= '3.4'",
        "gitpython==3.1.3",
        "humanfriendly==8.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "idna==2.9; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pygithub==1.51",
        "pyjwt==1.7.1",
        "requests==2.23.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "smmap==3.0.4; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "urllib3==1.25.9; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_version < '4'",
        "wrapt==1.12.1",
    ],
    extras_require={"dev": []},
    dependency_links=[],
    entry_points={"console_scripts": ["merger=merger.cli:merger_main"]},
)
