import os
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

# # Download the latest version of mirror-sync to the current folder
clientFileName = "mirror-sync.py"
try:
	downloadFile(clientFileName)
	print("Downloaded " + clientFileName)
except:
	print("Failed to download " + clientFileName)

# Download the latest version of mirror-update to the current folder
clientFileName = "mirror-update.py"
try:
	downloadFile(clientFileName)
	print("Downloaded " + clientFileName)
except:
	print("Failed to download " + clientFileName)

print(" ")
print("binfiles.net initial mirror installation is complete.")
print("Initial mirror file download is beinning momentarily.")
print("This initial download will take a few seconds to a few minutes depending on uplink speed.")

# Run mirror-sync for the first time to download all mirror data to the current folder
os.system("py mirror-sync.py")

print(" ")
print("binfiles.net mirror installation and initial mirror data download are complete.")
print(" ")
print("In the current working direction are the scripts necessary to:")
print(" * Download all mirror data files and hash files (mirror-sync.py)")
print(" * Update the mirror-sync script to the latest version (mirror-update.py)")
print(" ")
print("We recommend you setup a cron job to run mirror-sync.py regularly.")
print(" ")
print("When mirror-sync.py runs, it will delete files not needed for the mirror from")
print("the current folder. It will also check the file hashes of the data files and")
print("re-download any data files whose hashes are inconsistent. At this same time,")
print("any files added to the mirror-list will be downloaded along with their hashes.")
print("Files will not be re-downloaded unless inconsistencies are detected.")
print(" ")
print("The mirror-update.py script will download the latest version of mirror-sync.py.")
print("You can review the contents of mirror-sync.py script that will be downloaded:")
print("")
print("https://s3.binfiles.net/mirror-sync.py")
print(" ")
print("binfiles.net and mirror code are distributed under the MIT License.")
print("For project info, license details, and source code, visit:")
print(" ")
print("https://github.com/binfiles/binfiles.net/")
print(" ")
print("Thank you for hosting a binfiles.net mirror!")
print(" ")
