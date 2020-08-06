import requests
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

# Download the latest version of mirror-sync
clientFileName = "mirror-sync.py"
try:
	downloadFile(clientFileName)
	print("Downloaded " + clientFileName)
except:
	print("Failed to download " + clientFileName)
