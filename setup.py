from setuptools import setup

setup(
  name='jgen',
  version=open('VERSION').read().strip(),
  description='Generate simple JSON documents from the command line.',
  author='Jon McKenzie',
  license='BSD',
  url='https://github.com/jcmcken/jgen',
  packages=["jgen"],
  scripts=["bin/jgen"],
)
