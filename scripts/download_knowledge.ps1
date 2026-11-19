param(
    [Parameter(Mandatory = $true)]
    [string]$Url,
    [Parameter(Mandatory = $true)]
    [string]$OutputPath
)

$ErrorActionPreference = "Stop"

$uri = [Uri]$Url
if ($uri.Scheme -ne "https" -or (($uri.Host -notlike "*.go.th") -and ($uri.Host -notin @("ratchakitcha.soc.go.th", "www.ratchakitcha.soc.go.th")))) {
    throw "Only HTTPS URLs from official government or gazette domains are allowed"
}

$parent = Split-Path -Parent $OutputPath
if ($parent) {
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
}

$base = $parent
if (-not $base) { $base = (Get-Location).Path }
$stagingPath = Join-Path $base ([IO.Path]::GetRandomFileName())
try {
    Invoke-WebRequest -Uri $Url -OutFile $stagingPath -MaximumRedirection 8
    $bytes = [System.IO.File]::ReadAllBytes($stagingPath)
} catch {
    if (Test-Path -LiteralPath $stagingPath) { Remove-Item -LiteralPath $stagingPath -Force }
    throw
}

if ($OutputPath.ToLowerInvariant().EndsWith(".pdf")) {
    $signature = [System.Text.Encoding]::ASCII.GetString($bytes, 0, [Math]::Min(5, $bytes.Length))
    if ($signature -ne "%PDF-") {
        Remove-Item -LiteralPath $stagingPath -Force
        throw "Downloaded content is not a valid PDF"
    }
}

if (Test-Path -LiteralPath $OutputPath) {
    Copy-Item -LiteralPath $OutputPath -Destination "$OutputPath.previous" -Force
}
Move-Item -LiteralPath $stagingPath -Destination $OutputPath -Force
$hash = (Get-FileHash -LiteralPath $OutputPath -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Output "DOWNLOAD_OK SHA256=$hash PATH=$OutputPath"
