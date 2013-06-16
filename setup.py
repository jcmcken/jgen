from setuptools import setup, find_packages

setup(
  name='jgen',
  version=open('VERSION').read().strip(),
  packages=find_packages(),
  entry_points={
    'console_scripts': ['jgen = jgen:main']
  }
)
