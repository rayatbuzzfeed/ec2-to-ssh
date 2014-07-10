# -*- coding: utf-8 -*-
"""
    Licensed to the Apache Software Foundation (ASF) under one
    or more contributor license agreements.  See the NOTICE file
    distributed with this work for additional information
    regarding copyright ownership.  The ASF licenses this file
    to you under the Apache License, Version 2.0 (the
    "License"); you may not use this file except in compliance
    with the License.  You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing,
    software distributed under the License is distributed on an
    "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
    KIND, either express or implied.  See the License for the
    specific language governing permissions and limitations
    under the License.

"""

import ConfigParser
import os
import sys
from ec2_to_ssh.settings.SettingsKeys import *

HOME = os.getenv('HOME')
if sys.platform == 'win32':
    HOME = os.path.expanduser('~')

DEFAULT_CONFIGURATION_FILE = os.path.join(HOME, '.ec2ssh/settings.cfg')

class Settings(object):
    
    config = None
    settings = None
    
    def __init__(self, configuration_file=None):
        super(Settings, self).__init__()
        self.config = self._read_configuration(configuration_file)
        self.settings = self._initialize_settings()


    def _read_configuration(self, configuration_file=None):
        """
            Read the configuration file
        """
        # Check if we have received a different configuration file name
        if configuration_file is None:
            configuration_file = DEFAULT_CONFIGURATION_FILE

        # Check if the file even exists! If not, we have to write a default configuration file.
        if not os.path.exists(configuration_file):
            sys.exit('Configuration file {0} not found!'.format(configuration_file))

        # Read the configuration file
        configuration = ConfigParser.RawConfigParser()
        configuration.read(configuration_file)

        return configuration


    def _initialize_settings(self):
        """
            Read in ~/.ec2ssh/settings.cfg into settings dictionary
        """
        #noinspection PyDictCreation
        s = {}

        #
        # Defaults
        #
        s[SSH_PORT] = DEFAULT_SSH_PORT
        s[SSH_USER] = DEFAULT_SSH_USER
        s[EC2_AWS_ACCESS_KEY] = ''
        s[EC2_AWS_SECRET_ACCESS_KEY] = ''
        s[EC2_HOSTNAME_PREFIX] = ''
        s[EC2_AWS_DEFAULT_REGION] = ''
        s[DEBUGGING] = False

        #
        # SSH
        #
        s[SSH_KEY] = self.config.get(SSH_CONFIG_SECTION, SSH_KEY)
        if s[SSH_KEY] is None or not os.path.exists(s[SSH_KEY]):
            s[SSH_KEY] = os.path.join(HOME, DEFAULT_SSH_KEY)

        if self.config.has_option(SSH_CONFIG_SECTION, SSH_PORT):
            s[SSH_PORT] = self.config.get(SSH_CONFIG_SECTION, SSH_PORT)

        if self.config.has_option(SSH_CONFIG_SECTION, SSH_USER):
            s[SSH_USER] = self.config.get(SSH_CONFIG_SECTION, SSH_USER)

        #
        # EC2 ACCESS/SECRET KEYS
        #
        if os.environ.has_key(EC2_AWS_ACCESS_KEY):
            s[EC2_AWS_ACCESS_KEY] = os.environ[EC2_AWS_ACCESS_KEY]
        else:
            if self.config.has_option(EC2_SECTION, EC2_AWS_ACCESS_KEY):
                s[EC2_AWS_ACCESS_KEY] = self.config.get(EC2_SECTION, EC2_AWS_ACCESS_KEY)

        if os.environ.has_key(EC2_AWS_SECRET_ACCESS_KEY):
            s[EC2_AWS_SECRET_ACCESS_KEY] = os.environ[EC2_AWS_SECRET_ACCESS_KEY]
        else:
            if self.config.has_option(EC2_SECTION, EC2_AWS_SECRET_ACCESS_KEY):
                s[EC2_AWS_SECRET_ACCESS_KEY] = self.config.get(EC2_SECTION, EC2_AWS_SECRET_ACCESS_KEY)
        if self.config.has_option(EC2_SECTION, EC2_HOSTNAME_PREFIX):
            s[EC2_HOSTNAME_PREFIX] = self.config.get(EC2_SECTION, EC2_HOSTNAME_PREFIX)

        if self.config.has_option(EC2_SECTION, EC2_AWS_DEFAULT_REGION):
            s[EC2_AWS_DEFAULT_REGION] = self.config.get(EC2_SECTION, EC2_AWS_DEFAULT_REGION)
        #
        # DEBUG
        #
        if self.config.has_option(DEBUG_SECTION, DEBUGGING):
            s[DEBUGGING] = self.config.get(DEBUG_SECTION, DEBUGGING)

        return s



