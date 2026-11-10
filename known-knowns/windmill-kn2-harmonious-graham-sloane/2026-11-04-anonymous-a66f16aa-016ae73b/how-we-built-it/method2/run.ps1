param([int]$N=4,[bool]$Parity=$true,[double]$CapSeconds=60,[string]$Tag='calibration',[int]$FirstRoot=1,[int]$FinalRoot=0)
$ErrorActionPreference='Stop'
$attempt=Split-Path -Parent $PSScriptRoot
$progress=Join-Path $attempt ('output\'+$Tag+'.progress.jsonl')
$result=Join-Path $attempt ('output\'+$Tag+'.result.json')
$process=[Diagnostics.Process]::GetCurrentProcess()
$process.PriorityClass=[Diagnostics.ProcessPriorityClass]::BelowNormal
[IO.File]::AppendAllText((Join-Path $attempt 'output\processes.jsonl'),('{"pid":'+$PID+',"tag":"'+$Tag+'","utc":"'+[DateTime]::UtcNow.ToString('o')+'","priority":"BelowNormal","cap_seconds":'+$CapSeconds+'}'+[Environment]::NewLine))
Add-Type -Path (Join-Path $PSScriptRoot 'DirectConstraintWide.cs') -CompilerOptions '/optimize+'
$answer=[DirectConstraintWide]::Run($N,$Parity,$CapSeconds,$progress,$FirstRoot,$FinalRoot)
[IO.File]::WriteAllText($result,$answer+[Environment]::NewLine)
$answer
