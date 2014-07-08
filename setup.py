import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()

setup(
    name="fmlib",
    version="0.0.1",
    author="Hayden Crocker / Ben Field",
    author_email="hayden.james.crocker@gmail.com",
    description="A Python interface for the FileMaker API",
    license="BSD",
    keywords="filemaker fm xml",
    url="https://github.com/haydenc/FMLib",
    packages=['FMLib'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
