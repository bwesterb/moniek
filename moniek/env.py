# env.py
#   sets up the django environment
#

import os
import sys
import imp
import os.path

if __name__ != '__main__':
	os.environ['DJANGO_SETTINGS_MODULE'] = 'moniek.settings'
