param(
    [string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot)
)

$source = Join-Path $ProjectRoot "skills\tor-government-expert"
$target = Join-Path $ProjectRoot ".gemini\skills\tor-government-expert"
$stagingRoot = Join-Path $ProjectRoot "tmp\gemini-skill-stage"
$staging = Join-Path $stagingRoot "tor-government-expert"
$backup = Join-Path $ProjectRoot "tmp\gemini-skill-backup"

if (-not (Test-Path -LiteralPath $source)) {
    throw "Source skill not found: $source"
}

if (Test-Path -LiteralPath $stagingRoot) {
    Remove-Item -LiteralPath $stagingRoot -Recurse -Force
}
New-Item -ItemType Directory -Path (Split-Path -Parent $staging) -Force | Out-Null
Copy-Item -LiteralPath $source -Destination $staging -Recurse
if (-not (Test-Path -LiteralPath (Join-Path $staging "SKILL.md"))) {
    Remove-Item -LiteralPath $stagingRoot -Recurse -Force
    throw "Staged skill is incomplete"
}

try {
    if (Test-Path -LiteralPath $backup) {
        Remove-Item -LiteralPath $backup -Recurse -Force
    }
    if (Test-Path -LiteralPath $target) {
        Move-Item -LiteralPath $target -Destination $backup
    }
    New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force | Out-Null
    Move-Item -LiteralPath $staging -Destination $target
} catch {
    if (Test-Path -LiteralPath $target) {
        Remove-Item -LiteralPath $target -Recurse -Force
    }
    if (Test-Path -LiteralPath $backup) {
        Move-Item -LiteralPath $backup -Destination $target
    }
    throw
} finally {
    if (Test-Path -LiteralPath $stagingRoot) {
        Remove-Item -LiteralPath $stagingRoot -Recurse -Force
    }
}

Write-Output "GEMINI_SKILL_SYNC_OK PATH=$target"
