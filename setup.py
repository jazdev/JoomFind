#!/usr/bin/env python

from setuptools import setup, find_packages



setup(name='JoomFind',
      version='0.1',
      author='Jasdev Singh',
      author_email='jasdev@singh.am',
      licence='MIT',
      homepage='https://github.com/JoomFind',
      description='Automated detection of the Joomla! Content Management System',
      scripts=['JoomFind/JoomFind.py'],
      entry_points={
          'console_scripts':
              ['JoomFind = JoomFind.JoomFind:main']}
     )
