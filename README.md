# binfiles.net

## Overview

![Architecture Diagram](./docs/img/binfiles-architecture.svg)

## Public Website


## Data Files and Hash Files

This repo contains two type of files:  data files and file hashes.

The data files are created using random binary data in standard sizes that are distributed to binfiles.net mirrors around the world.  Users can request these files from mirrors to test their download speeds across various paths.

File hashes are available in three formats:  SHA256 (recommended), SHA1, and MD5.  Users can compare the hash from the mirror to the hash determined locally after download to ensure a complete, correct download occurred.  This helps the user check not only bandwidth but also connection integrity.

### Storage

Data Files and Hash Files are all stored on AWS S3 and accessible via s3.binfiles.net.  Please note that s3.binfiles.net should only be used for downloading the standard mirror data and not as a resource to perform network download tests.  Requests to s3.binfiles.net are cached through our CloudFlare CDN and will provide unpredictable results compared to network download tests initiated using binfiles.net mirrors.

### Data Files

Data files are created using binary byte sizes.  For example, 1MB = 1048576 Bytes or 500MB = 524288000 Bytes.

These are the sizes currently supported on binfiles.net mirrors:

1MB:	1048576

10MB:	10485760

100MB:	104857600

500MB:	524288000

1000MB:	1048576000

### File Hashes

Hashes of data files are provided as an option for verifying the integrity of downloads.  Hash files are hosted on all mirrors.

## Ensure all files on a mirror server are the latest versions

1. Login to the mirror server and navigate to the publicly accessible folder here mirror files are saved

1. Run `mirror-sync.py` to download:
   * All new data files and hash files not present on the mirror
   * Any files on the mirror whose local hash files are missing
   * Any files on the mirror whose hash files do not match the hash files on s3.binfiles.net
   * Any files whose locally computed hash does not match their previously downloaded hash files

1. Please note that `mirror-sync.py` will delete all files not needed by the mirror in the current folder -- if hosting on a server with other non-mirror content, the binfiles.net mirror data should be stored in a separate folder, such as //yourdomain.com/mirror/

## Setup a new mirror server

1. Ensure FTP and/or HTTP (not HTTPS) services are active on the mirror server

1. Ensure that `python3` and `pip` are installed on the mirror server

1. Create a new publicly accessible folder where the mirror files will be saved, such as //yourdomain.com/mirror/

1. Download the installer from https://s3.binfiles.net/mirror-setup.py

1. Run the `mirror-setup.py` script to download the mirror files
