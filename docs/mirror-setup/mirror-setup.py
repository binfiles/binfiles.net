import requests
import subprocess
import sys
import wget

# Describe the location of the mirror file list on the central distribution server
serverBaseURL = "https://s3.binfiles.net/"

# Helper function to download large files in streams
def downloadFile(filename):
	
	# Attempt the download
	response = requests.get(serverBaseURL + filename, stream = True)

	# If the download succeeded, write the data to a local file of the same name
	if response.status_code == 200:
		file = open("./" + filename,"wb")
		for chunk in response.iter_content(chunk_size=1024):
			file.write(chunk)
		file.close()
	else:
		raise Exception("Download failed (Error " + str(response.status_code) + "): " + serverBaseURL + filename)

# Helper function to install a named package via pip
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

# Download the latest version of mirror-sync
clientFileName = "mirror-sync.py"
try:
	downloadFile(clientFileName)
	print("Downloaded " + clientFileName)
except:
	print("Failed to download " + clientFileName)

# Download the latest version of mirror-update
clientFileName = "mirror-update.py"
try:
	downloadFile(clientFileName)
	print("Downloaded " + clientFileName)
except:
	print("Failed to download " + clientFileName)
