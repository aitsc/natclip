# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

if os.path.exists('readme.md'):
    long_description = open('readme.md', 'r', encoding='utf8').read()
else:
    long_description = """
作者:
    tanshicheng
包括:
    用于win,macos局域网内共享剪切板, 适用于moonlight等不支持剪切板的工具
"""

setup(
    name='natclip',
    version='0.6',
    description="tanshicheng's tools",
    long_description=long_description,
    author='tanshicheng',
    license='GPLv3',
    url='https://github.com/aitsc/natclip',
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
    entry_points={  # 打包到bin
        'console_scripts': [
            'natclip=natclip.main:main',  # 包不能有-符号
        ],
    },
)
