# ec2-to-ssh

This is the EC2-to-SSH tool taken from github user [otype](http://www.github.com/ec2-to-ssh/) and modified for my own settings.

## Latest version

The latest is `master`.

## Motivation

Got tired of updating my SSH configuration over and over again. This here simply reads out all *running* EC2 instances
and prints them out to screen.

## Installing ec2-to-ssh

Install via `pip`:

	$ easy_install pip
	$ pip install git+ssh://git@github.com/rayatbuzzfeed/ec2-to-ssh.git

## Configuring ec2-to-ssh

Before you can run `ec2-to-ssh` you must configure the appropriate configuration files

 * `${HOME}/.ec2ssh/settings.LIVE.cfg`
 * `${HOME}/.ec2ssh/settings.WEST.cfg`
 * `${HOME}/.ec2ssh/settings.DEV.cfg`
 * `${HOME}/.ec2ssh/settings.STAGE.cfg`

and fill in appropriate values for the corresponding EC2 environment. E.g. setting the correct SSH-Key
for the corresponding EC2 environment:

    [SSH_CONFIG]
    SSH_KEY = /Users/hgschmidt/.ssh/<your_ec2_ssh_key>
    SSH_PORT = 22
    SSH_USER = ubuntu

If you like you can set a prefix for all hostnames of a given EC2 environment. For instance, for your
DEV environment, you would like all hostnames to start with "dev-". To accomplish this, simply add a prefix
in the corresponding `settings.DEV.cfg` file

    EC2_HOSTNAME_PREFIX = dev

## Using ec2-to-ssh

Following descriptions gives instructions on how to use `ec2-to-ssh`.

### Environments

You have 3 possible environments to choose (add as parameter to `ec2-to-ssh`):

 1. live
 1. west
 2. dev
 3. stage

Calling `ec2-to-ssh` with one of the given environment identifiers will load the appropriate settings file:

	$ ec2-to-ssh dev


### Setting EC2 ACCESS/SECRET KEYS

You can either set environment variables and, then, call `ec2-to-ssh` with the corresponding EC2 environment:

	$ EC2_ACCESS_KEY=ABCDEFGHIJK EC2_SECRET_ACCESS_KEY=ALONGSECRETKEY ec2-to-ssh dev

Or you can set your Access Keys in the configuration file. E.g. setting your EC2 credentials for your DEV
environment will require changes in `${HOME}/.ec2ssh/settings.DEV.cfg`:

	[EC2]
    EC2_AWS_ACCESS_KEY = <put_your_key_key>
    EC2_AWS_SECRET_ACCESS_KEY = <put_your_secret_key_here>

Now call `ec2-to-ssh` with the 'dev' identifier:

	$ ec2-to-ssh dev

## Auto-update your SSH configuration

Simply create a shell function and add that to your shell configuration file (e.g. `~/.bashrc`):

	function update-ssh() {
	    EC2_AWS_ACCESS_KEY=<LIVE_KEY>  EC2_AWS_SECRET_ACCESS_KEY=<LIVE_SECRET_KEY>  ec2-to-ssh live  > ${HOME}/.ssh/config.liveplatform
	    EC2_AWS_ACCESS_KEY=<DEV_KEY>   EC2_AWS_SECRET_ACCESS_KEY=<DEV_SECRET_KEY>   ec2-to-ssh dev   > ${HOME}/.ssh/config.devplatform
	    EC2_AWS_ACCESS_KEY=<STAGE_KEY> EC2_AWS_SECRET_ACCESS_KEY=<STAGE_SECRET_KEY> ec2-to-ssh stage > ${HOME}/.ssh/config.stageplatform

	    touch ${HOME}/.ssh/config
	    mv ${HOME}/.ssh/config ${HOME}/.ssh/config_old

		for f in ${HOME}/.ssh/config.*
		do
	        cat $f >> ${HOME}/.ssh/config
	    done
	}

Now, all I need to do before logging in into an EC2 instance is to call `update-ssh`.

*NOTE:* `ec2-to-ssh` needs to be in your path when calling `update-ssh`!

### Using virtualenv

Simply source your `activate` script of your virtualenv at the beginning of the function:

	function update-ssh() {
		source ${WORKON_HOME}/ec2ssh/bin/activate

        [... update-ssh function content ...]

        deactivate
    }

## TODO

- dev, west, live, stage is available now ... but, possibly, there is a nicer solution.
