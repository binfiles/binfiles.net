import copy
import hashlib
import json
import os.path
from os import path

# Describe all sizes of files we need to create
dataFileSizes = [1048576, 10485760, 104857600, 524288000, 1048576000]

# Describe the hash types we'll be generating
hashFileTypes = ["sha256", "sha1", "md5"]

# Setup the stub object that will be used to record data and hash file details
serverFileStub = {
	"name": "",
	"size": 0,
	"hashes": []
}

# Setup the dictionary that will hold all data and hash file info
serverFiles = {
	"files" : []
}

# Iterate through all file sizes that we need to create
for size in dataFileSizes:

	# Setup the data file name from the size
	dataFileName = str(size) + ".bin"

	print("Creating " + dataFileName + " ... ", end="")

	# Start filling out the file stub
	newFile = copy.deepcopy(serverFileStub);
	newFile["name"] = dataFileName
	newFile["size"] = size

	# Attempt to delete the bin file if it exists
	if path.exists(dataFileName):
		try:
			os.remove(dataFileName)
		except:
			pass

	# Write binary content of the desired length to the dataFileName
	with open(dataFileName, 'wb') as f:
		num_chars = size
		f.write(b'0' * num_chars)

	for type in hashFileTypes:

		print("    Creating " + type + " hash for " + dataFileName + " ... ", end="")

		# Setup the hash file name from the size and hash type
		hashFileName = str(size) + "." + type

		# Save the hash type and filename to the new file stub
		newFile["hashes"].append({ "type": type, "filename": hashFileName })

		# Attempt to delete the hash file if it exists
		if path.exists(hashFileName):
			try:
				os.remove(hashFileName)
			except:
				pass

		# Detect the hash type and set up the hashlib worker for the next section

		if type == "sha256":
			file_hash = hashlib.sha256()

		elif type == "sha1":
			file_hash = hashlib.sha1()

		elif type == "md5":
			file_hash = hashlib.md5()

		# The size of each read from the file
		BLOCK_SIZE = 65536

		# Open, read, and hash the contents of the dataFileName
		with open(dataFileName, 'rb') as f:
			fb = f.read(BLOCK_SIZE)
			while len(fb) > 0:
				file_hash.update(fb)
				fb = f.read(BLOCK_SIZE)

		# Write the hash data to the hashFileName
		f = open(hashFileName, "w")
		f.write(file_hash.hexdigest())
		f.close()

		print("Done")

	# Now that all hashes for this file size are done, save the new file stub to the file dictionary
	serverFiles["files"].append(newFile)

# Save the server files dictionary as json
f = open("mirror-file-list.json", "w")
f.write(json.dumps(serverFiles))
f.close()