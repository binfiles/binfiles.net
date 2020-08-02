$dataFileSizes = 1048576, 10485760, 104857600, 524288000, 1048576000
$hashFileTypes = "sha256", "sha1", "md5"

foreach ($size in $dataFileSizes) {
	Write-Host "Creating $($size).bin ... "
	if (Test-Path "$($size).bin" -PathType Leaf) { del "$($size).bin" }
	fsutil file createNew "$($size).bin" $size
	foreach ($type in $hashFileTypes) {
		Write-Host "Creating $($type) hash for $($size).bin ... " -nonewline
		if ([System.IO.File]::Exists("$($size).$($type)")) { del "$($size).$($type)" }
		(Get-FileHash "$($size).bin" -Algorithm $($type) | Select-Object Hash) -Split "`n" -Replace "@{Hash=","" -Replace "}","" > "$($size).$($type)"
		Write-Host "Done"
	}
}