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

### Generate All Data Files and File Hashes

Run the generate.ps1 script, then upload the resulting .bin, .sha256, .sha1, .md5 files to the AWS S3 bucket.  After the latest files are available, then download the files to mirror servers.