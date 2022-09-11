# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

LONGDOC = """
作者:
    tanshicheng
包括:
    用于win,macos局域网内共享剪切板, 适用于moonlight
"""

setup(
    name='natclip',
    version='0.4',
    description="tanshicheng's tools",
    long_description=LONGDOC,
    author='tanshicheng',
    license='GPLv3',
    url='https://github.com/aitsc',
    keywords='tools',
    packages=find_packages(),

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'pyperclip>=1.7.0',
    ],
    python_requires='>=3.5',
)
