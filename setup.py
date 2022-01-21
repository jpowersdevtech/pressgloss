# -*- coding: utf-8 -*-

import setuptools
import os
from io import open

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
  readme_contents = f.read()

setuptools.setup(
  name='pressgloss',
  version='0.0.1',
  description='pressgloss library',
  long_description=readme_contents,
  long_description_content_type='text/x-rst',
  author='Joshua Powers',
  author_email='joshua.powers@devtechnology.com',
  install_requires=['flask'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Diplomacy Players',
    'Topic :: Analytics',
    'Programming Language :: Python :: 3.7'
  ],
  keywords='analytics',
  packages=setuptools.find_packages(),
  package_data={'':['resources/*.csv']},
  include_package_data=True,
  python_requires='>=3.7',
  entry_points = {'console_scripts': ['pressgloss=pressgloss.__main__:main']}
)
