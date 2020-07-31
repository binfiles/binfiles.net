$dataFileSizes = 1048576, 10485760, 104857600, 524288000, 1048576000

foreach ($size in $dataFileSizes) {
	del $size
	(Get-FileHash .\1048576.bin -Algorithm SHA256 | Select-Object Hash) -Split "`n" -Replace "@{Hash=","" -Replace "}","" > 1048576.sha256
	(Get-FileHash .\1048576.bin -Algorithm SHA1 | Select-Object Hash) -Split "`n" -Replace "@{Hash=","" -Replace "}","" > 1048576.sha1
	(Get-FileHash .\1048576.bin -Algorithm MD5 | Select-Object Hash) -Split "`n" -Replace "@{Hash=","" -Replace "}","" > 1048576.md5
}