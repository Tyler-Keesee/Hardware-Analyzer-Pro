param([switch]$Verify)

$setupArguments = @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", (Join-Path $PSScriptRoot "setup.ps1"), "-Development")
if ($Verify) { $setupArguments += "-Verify" }
& powershell.exe @setupArguments
exit $LASTEXITCODE
