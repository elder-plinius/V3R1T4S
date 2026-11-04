param([int]$Size,[int]$Seconds=600)
$ErrorActionPreference='Stop'
Add-Type -Path (Join-Path $PSScriptRoot 'independent.cs') -CompilerOptions '/optimize+'
[IndependentReproduce]::Run($Size,$Seconds)
