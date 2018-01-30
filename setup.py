import re

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'izk', '__init__.py')) as init:
    version = re.match(r"__version__ = '(.+)'", init.readline()).group(1)

setup(
    name='izk',
    version=version,
    description='Zookeeper CLI with autocomplete, syntax highlighting and pretty printing',
    long_description=long_description,
    url='https://github.com/brouberol/izk',
    author='Balthazar Rouberol;',
    author_email='br@imap.cc',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='zookeeper cli interactive',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
        'kazoo',
        'pygments',
        'prompt_toolkit',
        'colored'
    ],
    tests_require=[
        'pytest',
    ],
    entry_points={
        'console_scripts': [
            'izk=izk.prompt:main',
        ],
    },
)
