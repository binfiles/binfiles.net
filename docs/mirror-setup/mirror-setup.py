import subprocess
import sys

def install(package):
	try:
		subprocess.check_call([sys.executable, "-m", "pip", "install", package])
	except:
		print("pip must be installed before running this script.")
		print("wget https://bootstrap.pypa.io/get-pip.py | sudo py")
		print("or download and run https://bootstrap.pypa.io/get-pip.py")

packages = ["requests", "wget"]

for package in packages:
	install(package)