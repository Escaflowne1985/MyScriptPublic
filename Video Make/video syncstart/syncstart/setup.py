#!/usr/bin/env python

from setuptools import setup
import os
import ast
import re

here = os.path.abspath(os.path.dirname(__file__))
os.chdir(here)

_version_re = re.compile(r'__version__\s*=\s*(.*)')
with open(os.path.join(here, 'syncstart.py'), 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

with open(os.path.join(here, 'README.rst'), 'rt') as f:
    long_description = f.read()

setup(
    name="syncstart",
    version=version,
    description="Calculate the cut needed at start to sync two media files.",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    license="MIT",
    author="Roland Puntaier",
    author_email="roland.puntaier@gmail.com",
    url="https://github.com/rpuntaie/syncstart",
    py_modules=["syncstart"],
    data_files=[("man/man1", ["syncstart.1"])],
    install_requires=['numpy','scipy','matplotlib'],
    setup_requires=['stpl','restview'],
    python_requires='>=3.6',
    keywords='media file synchronization',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Topic :: Utilities',
        'Topic :: Multimedia',
        'Topic :: Multimedia :: Video',
        'Topic :: Multimedia :: Sound/Audio'
    ],
    entry_points="""
       [console_scripts]
       syncstart=syncstart:main
       """
)
