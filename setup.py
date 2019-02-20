from setuptools import setup

with open("README.md") as rd:
    long_description = rd.read()

VERSION = '0.1.0'

setup(
    name='plumber',
    author='Yoandy Rodriguez Martinez',
    author_email='yoandy.rmartinez@gmail.com',
    license='LICENSE',
    version=VERSION,
    packages=['plumber', ],
    long_description=long_description
)
