from setuptools import setup, find_packages

setup(
  name='jgen',
  version=open('VERSION').read().strip(),
  description='Generate simple JSON documents from the command line.',
  author='Jon McKenzie',
  license='BSD',
  url='https://github.com/jcmcken/jgen',
  packages=find_packages(),
  entry_points={
    'console_scripts': ['jgen = jgen:main']
  }
)
