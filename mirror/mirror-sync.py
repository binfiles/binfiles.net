import hashlib
import json
import os
import requests
import sys
import wget
from os import path
from urllib.request import urlopen, Request

# mirror-sync version: 2020-08-05(b)

# Describe the location of the mirror file list on the central distribution server
serverBaseURL = "https://s3.binfiles.net/"
serverFileList = "mirror-file-list.json"

# Collect the JSON data from the mirror file endpoint
request = requests.get(serverBaseURL + serverFileList)
response = json.loads(request.text)

print("")
if request.status_code == 200:
	print("Downloaded mirror list")
else:
	print("Failed to download mirror list from " + serverBaseURL + serverFileList)
	print("Sync cannot continue. Exiting ...")
	sys.exit(0)
print("")

# List of files that are valid for hosting on this mirror, verified with the server mirror list
validFileNames = []

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

print("Reviewing data files and hash files on the mirror list ...")
print(" ")

# Iterate over all files in the mirror list, check existence and validity, and download if needed
for remoteDataFile in response["files"]:

	# Add this data file name to the approved list of files to keep in the local folder
	validFileNames.append(remoteDataFile["filename"])
	
	# If the data file doesn't exist, download it
	if path.exists(remoteDataFile["filename"]) is False:
		print("Local copy of " + remoteDataFile["filename"] + " is missing")
		try:
			downloadFile(remoteDataFile["filename"])
			print("    Downloaded " + remoteDataFile["filename"])
		except:
			print("    Failed to download " + remoteDataFile["filename"])
	
	# If the data file exists, proceed with the hash checks
	if path.exists(remoteDataFile["filename"]):

		print("Local copy of " + remoteDataFile["filename"] + " exists")

		# Check all hashes associated with this data file
		for remoteHashFile in remoteDataFile["hashes"]:

			# Add this hash file name to the approved list of files to keep in the local folder
			validFileNames.append(remoteHashFile["filename"])

			# Download the hash from the main server
			remoteHashData = requests.get(serverBaseURL + remoteHashFile["filename"]).text

			# Detect the hash type and set up the hashlib worker for the next section
			if remoteHashFile["type"] == "sha256":
				hashMethod = hashlib.sha256()
			elif remoteHashFile["type"] == "sha1":
				hashMethod = hashlib.sha1()
			elif remoteHashFile["type"] == "md5":
				hashMethod = hashlib.md5()

			# The size of each read from the file
			BLOCK_SIZE = 65536

			# Open, read, and hash the contents of the remoteDataFileName
			with open(remoteDataFile["filename"], 'rb') as f:
				fb = f.read(BLOCK_SIZE)
				while len(fb) > 0:
					hashMethod.update(fb)
					fb = f.read(BLOCK_SIZE)

			# Check hash against server file and download it if it doesn't match
			if hashMethod.hexdigest() != remoteHashData:
				print("    Local copy of " + remoteDataFile["filename"] + " has incorrect " + remoteHashFile["type"] + " hash: " + remoteDataFile["filename"])
				downloadFile(remoteDataFile["filename"])
			else:
				print("    Local copy of " + remoteDataFile["filename"] + " has correct " + remoteHashFile["type"] + " hash")

			# Check whether local hash file exists and matches; if not, download it
			if path.exists(remoteHashFile["filename"]) is False:
				print("    Local " + remoteHashFile["type"] + " hash file is missing")
				try:
					downloadFile(remoteHashFile["filename"])
					print("        Downloaded " + remoteHashFile["filename"])
				except:
					print("        Failed to download " + remoteHashFile["filename"])
			else:
				with open(remoteHashFile["filename"], 'r') as localHashFile:
					localHashData = localHashFile.read().replace('\n', '')
				if localHashData != remoteHashData:
					print("    Local " + remoteHashFile["type"] + "hash file is incorrect: " + remoteHashFile["filename"])
					try:
						downloadFile(remoteHashFile["filename"])
						print("        Downloaded " + remoteHashFile["filename"])
					except:
						print("        Failed to download " + remoteHashFile["filename"])
				else:
					print("    Local " + remoteHashFile["type"] + " hash file matches server version for " + remoteDataFile["filename"])

print(" ")
print("Verifying filenames in current folder ...")
print(" ")

# Get a list of all files in the current folder
folder = "./"
localFiles = os.listdir(folder)

# Iterate over all files in this folder, check if found in list of authoritative files, delete if not
for localFile in localFiles:
	
	print("Checking " + localFile + " ... ")

	# Files with *.py extension are OK
	if localFile.endswith(".py") is False:

		# Files in validFileNames list are OK
		if localFile not in validFileNames:

			# Delete the file since it doesn't match the required criteria
			os.remove(os.path.join(folder, localFile))
			print("    Deleted " + localFile + " (not present in mirror list)")

		else:
			print("    File is in mirror list, verified")

	else:
		print("    File has *.py extension, skipping")
