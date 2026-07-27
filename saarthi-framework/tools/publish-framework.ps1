param(
  [Parameter(Mandatory = $true)]
  [string]$SourcePath,

  [string]$DestinationPath,

  [switch]$Force
)

if ([string]::IsNullOrEmpty($DestinationPath)) {
  $DestinationPath = Split-Path -Parent $PSScriptRoot
}

$ErrorActionPreference = "Stop"

$PythonBin = $null
if (Get-Command py -ErrorAction SilentlyContinue) {
  $PythonBin = "py"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
  $PythonBin = "python"
} else {
  throw "Python 3 is required but was not found in PATH."
}

if (-not (Test-Path $SourcePath)) {
  throw "Source path not found: $SourcePath"
}

if (-not (Test-Path $DestinationPath)) {
  New-Item -ItemType Directory -Path $DestinationPath -Force | Out-Null
}

$srcFull = (Resolve-Path $SourcePath).Path.TrimEnd('\\')
$destFull = (Resolve-Path $DestinationPath).Path.TrimEnd('\\')
if ($srcFull -eq $destFull) {
  throw "Source and destination are the same path."
}

$signature = @(
  "framework.config.yaml",
  "manifest.json",
  "AGENTS.md",
  "_framework",
  "templates",
  "tools"
)
$found = @()
foreach ($rel in $signature) {
  $p = Join-Path $SourcePath $rel
  if (Test-Path $p) { $found += $rel }
}

$score = 0
if ($signature.Count -gt 0) {
  $score = [math]::Round(($found.Count / $signature.Count), 2)
}

if ($score -lt 0.5 -and -not $Force) {
  Write-Host "Guardrail: source path looks very different from expected framework structure." -ForegroundColor Yellow
  Write-Host "Source: $SourcePath"
  Write-Host "Detected signature entries: $($found -join ', ')"
  Write-Host "Similarity score: $score (threshold: 0.5)"
  $confirm = Read-Host "Proceed anyway? Type YES to continue"
  if ($confirm -ne "YES") {
    throw "Publish cancelled by guardrail."
  }
}

Get-ChildItem -Path $DestinationPath -Force | Remove-Item -Recurse -Force
Copy-Item -Path (Join-Path $SourcePath "*") -Destination $DestinationPath -Recurse -Force

$required = @(
  "framework.config.yaml",
  "_framework\INDEX.md",
  "tools\validate_work_item.py"
)

$missing = @()
foreach ($rel in $required) {
  $p = Join-Path $DestinationPath $rel
  if (-not (Test-Path $p)) {
    $missing += $rel
  }
}

if ($missing.Count -gt 0) {
  Write-Host "Publish completed, but required files are missing:" -ForegroundColor Yellow
  $missing | ForEach-Object { Write-Host " - $_" -ForegroundColor Yellow }
  exit 2
}

Write-Host "Publish successful." -ForegroundColor Green
Write-Host "Source:      $SourcePath"
Write-Host "Destination: $DestinationPath"
Write-Host "Validator:   $PythonBin `"$DestinationPath\tools\validate_work_item.py`" <WORK_ITEM_ID> --root `"$DestinationPath`""
if ($Force) {
  Write-Host "Guardrail override was used (--Force)." -ForegroundColor Yellow
}

Write-Host "Running post-publish smoke test..." -ForegroundColor Cyan
$smokeScript = Join-Path $DestinationPath "tools\smoke_test_framework.py"
if (Test-Path $smokeScript) {
  if ($PythonBin -eq "py") {
    & py -3 $smokeScript --root $DestinationPath
  } else {
    & python $smokeScript --root $DestinationPath
  }
  if ($LASTEXITCODE -ne 0) {
    Write-Host "Publish completed but smoke test failed." -ForegroundColor Yellow
    exit 3
  }
} else {
  Write-Host "Smoke-test helper not found after publish; running fallback smoke check." -ForegroundColor Yellow
  if ($PythonBin -eq "py") {
    & py -3 (Join-Path $DestinationPath "tools\validate_work_item.py") --help | Out-Null
  } else {
    & python (Join-Path $DestinationPath "tools\validate_work_item.py") --help | Out-Null
  }
  if ($LASTEXITCODE -ne 0) {
    Write-Host "Publish completed but fallback smoke test failed." -ForegroundColor Yellow
    exit 3
  }
}

Write-Host "Post-publish smoke test passed." -ForegroundColor Green
