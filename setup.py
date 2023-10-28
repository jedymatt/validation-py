from setuptools import setup, find_packages
from validation import __version__


setup(name="validation-py", version=__version__, packages=find_packages(include=["validation", "validation.*"]))
