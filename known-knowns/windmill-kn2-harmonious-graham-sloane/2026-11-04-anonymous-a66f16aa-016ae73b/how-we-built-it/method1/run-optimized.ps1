param(
    [Parameter(Mandatory=$true)][int]$N,
    [Parameter(Mandatory=$true)][string]$OutputPrefix,
    [double]$CapSeconds=60,
    [double]$MemoryCapMiB=512,
    [int]$FirstMin=1,
    [int]$FirstMax=0
)
$ErrorActionPreference='Stop'
[Diagnostics.Process]::GetCurrentProcess().PriorityClass='BelowNormal'
Add-Type -Path (Join-Path $PSScriptRoot 'ComplementSearch.cs') -CompilerOptions '/optimize+'
[ComplementSearch]::Run($N,$CapSeconds,$MemoryCapMiB,$FirstMin,$FirstMax,$OutputPrefix)
