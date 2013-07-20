#!/usr/bin/env python

from distutils.core import setup

setup(name='flavorite',
      version='0.1',
      url='https://github.com/faithlessfriend/flavorite',
      author='Andrei Zhabinski',
      author_email='github_nickname@gmail.com',
      description='Simple item-based recommender',
      platforms='any',
      packages=['flavorite'],
      requires=['SciPy (>=0.10)'],
  )