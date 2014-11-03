#!/usr/bin/env python

from setuptools import setup

setup(name='nanogenmo',
      version='1.0',
      description="Moss's NaNoGenMo Novel",
      author='Moss Collum',
      author_email='moss@makingcodespeak.com',
      packages=['nanogenmo'],
      requires=[
          'textblob',
          'pytest',
          ],
      entry_points={
          'console_scripts': [
              'meatify = nanogenmo.cli:meatify_cmd'
          ],
      },
     )
