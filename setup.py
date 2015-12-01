#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
setuptools config file
"""

import sys
import pip
from pip.req import parse_requirements
from setuptools import setup, find_packages
import os
from snaplayer import __version


# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt', session=pip.download.PipSession())

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name=PKG_NAME,
    version=__version,
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    author="Alejandro Ricoveri",
    author_email="alejandroricoveri@gmail.com",
    description="Softlayer instances snapshots",
    long_description=open('README.rst').read(),
    url=PKG_URL,
    license='MIT',
    download_url="{url}/tarball/{version}".format(url=PKG_URL, version=__version),
    keywords=['softlayer', 'backup'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console	',
        'Topic :: Database',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.3',
    ],
    entry_points={
        'console_scripts': [
            'snaplayer = snaplayer.app:main',
        ],
    },
    install_requires = reqs,
)
