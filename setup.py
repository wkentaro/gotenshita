#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
import subprocess
from setuptools import setup
from setuptools import find_packages


# publish helper
if sys.argv[-1] == 'publish':
    for cmd in [
            'python setup.py sdist upload',
            'git tag {}'.format(__import__('gotenshita').__version__),
            'git push origin master --tag']:
        subprocess.check_call(cmd, shell=True)
    sys.exit(0)

setup(
    name='gotenshita',
    version=__import__('gotenshita').__version__,
    packages=find_packages(),
    description='Gotenshita notifier.',
    long_description=open('README.rst').read(),
    author='Kentaro Wada',
    author_email='www.kentaro.wada@gmail.com',
    url='http://github.com/wkentaro/gotenshita',
    install_requires=open('requirements.txt').readlines(),
    license='MIT',
    keywords='utility',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Topic :: Internet :: WWW/HTTP',
    ],
    entry_points={'console_scripts': ['gotenshita=gotenshita.cli:main']},
    test_suite='nose.collector',
)
