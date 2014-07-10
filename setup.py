#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    setup script EC2-TO-SSH

    usage: sudo python setup.py install
"""

from distutils.core import setup
import os
from setuptools import find_packages
import sys
import version

required = ['boto']

DOWNLOAD_URL = 'https://github.com/downloads/otype/ec2-to-ssh/ec2-too-ssh-{0}.tar.gz'.format(version.__version__)

# Read the $HOME variable! Overwrite it if we're on Windows.
HOME = os.getenv('HOME')
if sys.platform == 'win32':
    HOME = os.path.expanduser('~')

def get_data_files():
    """
        We don't want to overwrite the ~/.ec2ssh/settings.cfg over and over again upon
        update of EC2-TO-SSH. Instead, we should check if it already exists and, then,
        install it if necessary.
    """
    configuration_file = os.path.join(HOME, '.ec2ssh/settings.cfg')
    if os.path.exists(configuration_file):
        print "Configuration file {0} found! Skipping creation!".format(configuration_file)
        return []
    return [
        (os.path.join(os.environ['HOME'], '.ec2ssh'), ['src/ec2_to_ssh/conf/settings.LIVE.cfg']),
        (os.path.join(os.environ['HOME'], '.ec2ssh'), ['src/ec2_to_ssh/conf/settings.DEV.cfg']),
        (os.path.join(os.environ['HOME'], '.ec2ssh'), ['src/ec2_to_ssh/conf/settings.STAGE.cfg']),
    ]


# Extra options can be set here without cluttering the setup() method.
extra_options = dict(
    # Nothing
)

setup(
    name="ec2-to-ssh",
    version=version.__version__,
    description='ec2-to-ssh',
    author='Hans-Gunther Schmidt',
    author_email='hgs@cloudcontrol.de',
    url='https://www.cloudcontrol.com',
    install_requires=required,
    packages=find_packages('src'),
    package_dir={'' : 'src'},
    scripts=['src/ec2-to-ssh', 'src/ec2-instances.py'],
    data_files=get_data_files(),
    download_url=DOWNLOAD_URL,
    license='Apache 2.0',
    **extra_options
)
