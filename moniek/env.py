# env.py
#   sets up the django environment and mailman for the utils
#

import os
import sys
import imp
import os.path

if __name__ != '__main__':
	os.environ['DJANGO_SETTINGS_MODULE'] = 'moniek.settings'
