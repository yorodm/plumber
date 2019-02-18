from setuptools import setup

with open("README.md") as rd:
    long_description = rd.read()

VERSION = '0.1dev'

setup(
    name='plumber',
    version=VERSION,
    packages=['plumber', ],
    license='MIT',
    long_description=long_description
)
