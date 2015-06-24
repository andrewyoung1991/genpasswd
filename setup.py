import os.path
from setuptools import setup, find_packages

def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as _f:
        contents = _f.read()
    return contents

setup(
    name="genpasswd",
    version="0.1",
    author="andrew young",
    author_email="ayoung@thewulf.org",
    description="generate and retrieve complex passwords with a master password and a keyword.",
    keywords="password security",
    long_description=read("README.md"),
    packages=find_packages(exclude=["tests", "tests.*"]),
    test_suite="tests",
    install_requires=["pyperclip"],
    entry_points={
        "console_scripts": [
            "genpasswd = genpasswd.genpasswd:main"
        ]
    }
)
