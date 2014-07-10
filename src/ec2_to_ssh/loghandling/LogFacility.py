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

import logging
import os

class LogFacility(object):
    log_levels   = ['DEBUG', 'INFO', 'WARNING', 'ERROR']

    logger       = 'main'
    log_format   = '%(asctime)-15s %(name)s %(levelname)s %(message)s'
    log_dir      = os.path.join(os.environ['HOME'], '.ec2ssh')
    log_filename = '{0}.log'.format(logger)


    def __init__(self):
        """
            Initialize LogFacility
        """
        super(LogFacility, self).__init__()

        self.log_formatter = logging.Formatter(self.log_format)
        self.log_file      = '{0}/{1}'.format(self.log_dir, self.log_filename)
        self.log_handler   = logging.FileHandler(self.log_file)
        self.log_handler.setFormatter(self.log_formatter)


    def get_logger(self, logger=None):
        """
            Create the logger object and return it back
        """
        if logger is None:
            logger = self.logger

        log = logging.getLogger(logger)
        log.addHandler(self.log_handler)
        log.setLevel(logging.DEBUG)

        return log
