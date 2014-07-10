#!/usr/bin/env python
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

import sys
from ec2_to_ssh.aws.EC2SSH import EC2SSH
from ec2_to_ssh.loghandling.LogFacility import LogFacility
from ec2_to_ssh.messages.Messages import err
from ec2_to_ssh.settings.Settings import Settings
from ec2_to_ssh.settings.SettingsKeys import DEBUGGING
from ec2_to_ssh.settings.SettingsKeys import EC2_AWS_ACCESS_KEY
from ec2_to_ssh.settings.SettingsKeys import EC2_AWS_SECRET_ACCESS_KEY

####################################################################
#
# CONFIGURATION PARAMETERS
#
####################################################################

# Logger
log = LogFacility().get_logger()

# Global settings dictionary
SETTINGS = Settings().settings

# If set to True, additional debug messages will be printed out
DEBUG = SETTINGS[DEBUGGING]

####################################################################
#
# FUNCTIONS
#
####################################################################

def main():
    if SETTINGS[EC2_AWS_ACCESS_KEY] == '':
        sys.exit(err['ERR_NO_EC2_ACCESS_KEYS'])

    ec2ssh = EC2SSH(
        SETTINGS[EC2_AWS_ACCESS_KEY],
        SETTINGS[EC2_AWS_SECRET_ACCESS_KEY]
    )

    print ec2ssh.print_instances()


####################################################################
#
# MAIN
#
####################################################################

if __name__ == "__main__":
    main()
