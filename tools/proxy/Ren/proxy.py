#!/home/s/ops/Python-3.5.6/python

import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from Ren.load import load


# Use private key to sign a message
# Return Value:
#   On success, return signature
#   On failure, return None
def sign(message):
	confDict = load()
	key = os.path.join(confDict['auth'], 'rsa.key')
	passwd = confDict['passwd'].encode()

	with open(key, "rb") as key_file:
		private_key = serialization.load_pem_private_key(
			key_file.read(),
			#password=None,
			password=passwd,
			backend=default_backend()
		)
	
	if not isinstance(message, bytes):
		print('sign() arguments should be bytes object')
		return None

	signature = private_key.sign(
		message,
		padding.PSS(
			mgf=padding.MGF1(hashes.SHA256()),
			salt_length=padding.PSS.MAX_LENGTH
		),
		hashes.SHA256()
	)

	return signature

# Use public key to vertify a signature
# Return Value:
#   On success, return True
#   On failure, return False
def verify(sign, message):
	if not (isinstance(sign, bytes) and isinstance(message, bytes)):
		print("vertify() arguments should be bytes object")
		return False

	confDict = load()
	key = os.path.join(confDict['auth'], 'rsa.pub')

	with open(key, "rb") as key_file:
		public_key = serialization.load_pem_public_key(
			key_file.read(),
			backend=default_backend()
		)


	try:
		public_key.verify(
			sign,
			message,
			padding.PSS(
				mgf=padding.MGF1(hashes.SHA256()),
				salt_length=padding.PSS.MAX_LENGTH
			),
			hashes.SHA256()
		)
	except InvalidSignature:
		return False

	return True

# Run plugin code
def run(argv):
	argvDict = yaml.load(argv)
	code = argvDict['code']

	confDict = load()
	codefile = os.path.join(confDict['code'], code)
	exec(open(codefile).read(), argvDict)
