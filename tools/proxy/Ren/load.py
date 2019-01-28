#!/home/s/ops/Python-3.5.6/python

import os
import sys
import yaml
from os.path import isfile


# Inspired by Perl module FindBin
Bin        = os.path.dirname(sys.argv[0])
Script     = os.path.basename(sys.argv[0])
RealBin    = os.path.dirname(os.path.realpath(sys.argv[0]))
RealScript = os.path.basename(os.path.realpath(sys.argv[0]))

THIS = RealScript

# Load yaml config file and only return the section that specified by `THIS`
# In addition, do the following thing:
#   - Expand '$ROOT' macro
def load(conf=None):
	if conf is None:
		conf = RealBin + "/.config" if isfile(RealBin + "/.config") else RealBin + "/../.config"
		if not isfile(conf):
			print("Error: Not find config file.")
			exit(1)

	fin = open(conf)
	confDict = yaml.load(fin)
	fin.close()

	confRealPath = os.path.realpath(conf)
	ROOT = os.path.dirname(os.path.dirname(confRealPath))
	for key in confDict[THIS].keys():
		if isinstance(confDict[THIS][key], str) and '$ROOT' in confDict[THIS][key]:
			confDict[THIS][key] = confDict[THIS][key].replace('$ROOT', ROOT)
	return confDict[THIS]
