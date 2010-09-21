# _import.py
#   sets up the django environment and mailman for the utils
#

import os
import sys
import imp
import os.path

def setup_virtual_package(name, path=os.curdir):
	""" Sets up a package at the given path with a given
	    name """
	modulePath = os.path.abspath(path)
	f, fn, suffix = imp.find_module('__init__',
		 [modulePath])
	imp.load_module(name, f, fn, suffix)
	sys.modules[name].__path__ = [modulePath]


if __name__ != '__main__':
	os.environ['DJANGO_SETTINGS_MODULE'] = 'moniek.settings'
	path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(
		os.path.realpath(__file__[:-1] if __file__[-4:] in 
			('.pyc', '.pyo') else __file__))), '../moniek'))
	setup_virtual_package('moniek', path)
