# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
#     long_description = f.read()


setup(
    name='izk',  # Required
    version='0.1.0',  # Required
    description='Zookeeper CLI with autocomplete, syntax highlighting and pretty printing',
    # long_description=long_description,
    url='https://github.com/brouberol/izk',
    author='Balthazar Rouberol;',
    author_email='br@imap.cc',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache 2.0 License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='zookeeper cli interactive',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
    install_requires=[
        'kazoo',
        'pygments',
        'prompt_toolkit'
    ],  # Optional
    entry_points={  # Optional
        'console_scripts': [
            'izk=izk.prompt:main',
        ],
    },
)
