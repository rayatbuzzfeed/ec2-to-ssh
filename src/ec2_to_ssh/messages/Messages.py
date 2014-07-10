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

#
# REGULAR MESSAGES
#
#noinspection PyDictCreation
msg = {}


#
# ERROR MESSAGES
#
#noinspection PyDictCreation
err = {}
err['ERR_NO_EC2_ACCESS_KEYS'] = '''No AWS access keys found!

Please do one of the following:

Option #1: Set environment variables

  $ export EC2_AWS_ACCESS_KEY=<your_access_key>
  $ export EC2_AWS_SECRET_ACCESS_KEY=<your_secret_access_key>

Option #2: Add your credentials to ~/.ec2ssh/settings.cfg

  $ vi ~/.ec2ssh/settings.cfg

  [EC2]
  EC2_AWS_ACCESS_KEY = <your_access_key>
  EC2_AWS_SECRET_ACCESS_KEY = <your_secret_access_key>

'''

err['ERR_CANNOT_CONNECT_TO_AWS'] = '''Cannot connect to AWS!'''
err['ERR_NO_INSTANCES_FOUND'] = ''''No EC2 instances found! Make sure you are connecting to the right region!'''
