# binfiles.net

## Public Website



## Data Files and Hash Files

This repo contains two type of files:  data files and file hashes.

The data files are created using random binary data in standard sizes that are distributed to binfiles.net mirrors around the world.  Users can request these files from mirrors to test their download speeds across various paths.

File hashes are available in three formats:  SHA256 (recommended), SHA1, and MD5.  Users can compare the hash from the mirror to the hash determined locally after download to ensure a complete, correct download occurred.  This helps the user check not only bandwidth but also connection integrity.

### Storage

Data Files and Hash Files are all stored on AWS S3 and accessible via s3.binfiles.net.  Please note that s3.binfiles.net should only be used for downloading the standard mirror data and not as a resource to perform network download tests.  Requests to s3.binfiles.net are cached through our CloudFlare CDN and will provide unpredictable results compared to network download tests initiated using binfiles.net mirrors.

### Data Files

Data files are created using binary byte sizes.  For example, 1MB = 1048576 Bytes or 500MB = 524288000 Bytes.

The data files were generated using this command with a 1MB data file as an example:

    fsutil file createNew 1048576.bin 1048576

These are the sizes currently supported on binfiles.net mirrors:

1MB:	1048576

10MB:	10485760

100MB:	104857600

500MB:	524288000

1000MB:	1048576000

### File Hashes

These are the commands used to generate each file hash with the 1MB data file as an example:

SHA256:

    (Get-FileHash .\1048576.bin -Algorithm SHA256 | Select-Object Hash) -Split "`n" -Replace "@{Hash=","" -Replace "}","" > 1048576.sha256

SHA1:

    (Get-FileHash .\1048576.bin -Algorithm SHA1 | Select-Object Hash) -Split "`n" -Replace "@{Hash=","" -Replace "}","" > 1048576.sha1

MD5:

    (Get-FileHash .\1048576.bin -Algorithm MD5 | Select-Object Hash) -Split "`n" -Replace "@{Hash=","" -Replace "}","" > 1048576.md5

### Generate and upload entirely new data and hash files

1. Navigate to `/mirror`

1. Run `s3-generate.ps1` to create all of the `.bin`, `.sha256`, `.sha1`, and `.md5` files

1. Run `s3-upload.ps1` to upload the contents of `/mirror` to `s3.binfiles.net`

1. In CloudFlare, use the Purge Cache function to clear out old file versions

## Ensure all files on a mirror server are the latest versions

1. Login to the mirror server and navigate to the publicly accessible folder here mirror files are saved

1. Run `mirror-sync.ps1` to download:
   * All new data files and hash files not present on the mirror
   * Any files on the mirror whose local hash files are missing
   * Any files on the mirror whose hash files do not match the hash files on s3.binfiles.net
   * Any files whose locally computed hash does not match their previously downloaded hash files

## Setup a new mirror server

1. Ensure FTP and/or HTTP (not HTTPS) services are active on the mirror server

1. Choose a publicly accessible folder where the mirror files will be saved

1. Run the `mirror-download.ps1` script to download the latest files to a mirror server
