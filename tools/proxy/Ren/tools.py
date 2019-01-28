#!/home/s/ops/Python-3.5.6/python

import os
import sys
import subprocess
import requests
import datetime
import smtplib
import yaml
import hashlib
from email.mime.text import MIMEText
from email.header import Header
from os.path import isfile


# Inspired by Perl module FindBin
Bin        = os.path.dirname(sys.argv[0])
Script     = os.path.basename(sys.argv[0])
RealBin    = os.path.dirname(os.path.realpath(sys.argv[0]))
RealScript = os.path.basename(os.path.realpath(sys.argv[0]))


# Load yaml config file
def load(conf=None):
	if conf is None:
		conf = RealBin + "/.config" if isfile(RealBin + "/.config") else RealBin + "/../.config"
		if not isfile(conf):
			print("Error: Not find config file.")
			exit(1)

	fin = open(conf)
	confDict = yaml.load(fin)
	fin.close()

	return confDict

# Dump dict to yaml
def dict2yaml(dict_):
	print("---")

	if bool(dict_):
		print(yaml.dump(dict_, default_flow_style=False, allow_unicode=True), end='')

# Dump dict to yaml and remove empty line in output
def dict2yaml_noblank(dict_):
	print("---")

	if bool(dict_):
		output = yaml.dump(dict_, default_flow_style=False, allow_unicode=True)
		output = os.linesep.join([s for s in output.splitlines() if s])
		print(output)


# Convert range expr to python list
def range2list(Range):
    cmd = "Prange -l {0}".format(Range)
    cmdRes = subprocess.check_output(cmd, shell=True)
    List = cmdRes.decode('utf8').strip().split()
    return List

# Convert python list to range expr
def list2range(List):
    cmd = "Prange {0}".format(','.join(List))
    cmdRes = subprocess.check_output(cmd, shell=True)
    Range = cmdRes.decode('utf8').strip()
    return Range
