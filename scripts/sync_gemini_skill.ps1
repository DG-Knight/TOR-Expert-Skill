param(
    [string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot)
)

$source = Join-Path $ProjectRoot "skills\tor-government-expert"
$target = Join-Path $ProjectRoot ".gemini\skills\tor-government-expert"

if (-not (Test-Path -LiteralPath $source)) {
    throw "Source skill not found: $source"
}

if (Test-Path -LiteralPath $target) {
    Remove-Item -LiteralPath $target -Recurse -Force
}
New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force | Out-Null
Copy-Item -LiteralPath $source -Destination $target -Recurse

Write-Output "GEMINI_SKILL_SYNC_OK PATH=$target"
