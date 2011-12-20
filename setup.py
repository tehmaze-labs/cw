#!/usr/bin/env python

from distutils.core import setup

setup(name='cw',
      version='0.1',
      description='Continuous Wave (Morse)',
      long_description='''
About
=====

This module allows you to generate CW (morse) signals on a set frequency
and speed.

Example Usage
=============

::

    >>> from cw import Morse
    >>> morse = Morse(speed=8)
    >>> morse.play('Hello world')

Bugs/Features
=============

You can issue a ticket in GitHub: https://github.com/tehmaze/cw/issues
''',
      author='Wijnand Modderman',
      author_email='python@tehmaze.com',
      url='http://github.com/tehmaze/cw',
      packages = ['cw'],
     )
