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

import boto.ec2
import sys
from ec2_to_ssh.loghandling.LogFacility import LogFacility
from ec2_to_ssh.messages.Messages import err
from ec2_to_ssh.settings.Settings import Settings
from ec2_to_ssh.settings.SettingsKeys import SSH_PORT, SSH_KEY, SSH_USER, EC2_HOSTNAME_PREFIX, EC2_AWS_DEFAULT_REGION

####################################################################
# CONFIGURATION PARAMETERS
####################################################################

# Logger
log = LogFacility().get_logger()

# Global settings dictionary
SETTINGS = Settings().settings

####################################################################
# CLASS
####################################################################

class MissingAWSCredentialsException(Exception):
    def __init__(self, *args, **kwargs):
        super(MissingAWSCredentialsException, self).__init__(*args, **kwargs)

    def __str__(self):
        return super(MissingAWSCredentialsException, self).__str__()


class EC2SSH(object):
    # EC2 access keys
    ec2_aws_access_key = ''
    ec2_aws_secret_key = ''

    # list of EC2 instances
    instances = {}

    # the connection to Amazon
    connection = None

    def __init__(self, access_key, secret_key):
        if access_key is None or secret_key is None:
            raise MissingAWSCredentialsException(err['ERR_NO_EC2_ACCESS_KEYS'])

        self.ec2_aws_access_key = access_key
        self.ec2_aws_secret_key = secret_key
        self._connect()
        self._refresh_instances()

    def _connect(self):
        try:
            self.connection = boto.ec2.connect_to_region(
                region_name=SETTINGS[EC2_AWS_DEFAULT_REGION],
                aws_access_key_id=self.ec2_aws_access_key,
                aws_secret_access_key=self.ec2_aws_secret_key
            )
        except boto.exception.EC2ResponseError, e:
            log.error(err['ERR_CANNOT_CONNECT_TO_AWS'])
            log.debug(e)
            sys.exit(err['ERR_CANNOT_CONNECT_TO_AWS'])

        return self.connection

    def _refresh_instances(self):
        """
        Get a list of all instances
        """
        reservations = self.connection.get_all_instances()
        instances = [i for r in reservations for i in r.instances]
        instances.sort()

        self.instances = instances

        #noinspection PySimplifyBooleanCheck
        if len(instances) == 0:
            sys.exit(err['ERR_NO_INSTANCES_FOUND'])

        return self.instances

    def print_instances(self):
        ssh_config = ''
        for instance in self.instances:
            if instance.state == 'running':
                try:
                    name = instance.tags['Name']
                except KeyError:
                    continue

                ssh_port = SETTINGS[SSH_PORT]
                if name.startswith('lb-') or name.startswith('loadbalancer-'):
                    ssh_port = 2222

                hostname = str(name).partition(' ')[0]
                if SETTINGS[EC2_HOSTNAME_PREFIX] is not '':
                    hostname = '{0}-{1}'.format(
                        SETTINGS[EC2_HOSTNAME_PREFIX],
                        hostname
                    )

                ssh_config += """
host {hostname}
        hostname {public_dns_name}
        port {ssh_port}
        identityfile {id_file}
        user {user}
""".format(
                    hostname=hostname,
                    public_dns_name=instance.ip_address,
                    ssh_port=ssh_port,
                    id_file="~/.ssh/" + instance.key_name +".pem",
                    user=SETTINGS[SSH_USER]
                )

        return ssh_config
