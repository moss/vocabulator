#!/usr/bin/env python

from setuptools import setup

setup(name='vocabulator',
      version='1.0',
      description="Moss's NaNoGenMo Novel",
      author='Moss Collum',
      author_email='moss@makingcodespeak.com',
      packages=['vocabulator'],
      requires=[
          'textblob',
          'pytest',
          'docopt',
      ],
      entry_points={
          'console_scripts': [
              'vocabulator = vocabulator.cli:vocabulator',
          ],
      },
      )
