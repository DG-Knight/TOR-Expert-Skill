param(
    [Parameter(Mandatory = $true)]
    [string]$Url,
    [Parameter(Mandatory = $true)]
    [string]$OutputPath
)

$ErrorActionPreference = "Stop"

$parent = Split-Path -Parent $OutputPath
if ($parent) {
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
}

Invoke-WebRequest -Uri $Url -OutFile $OutputPath -MaximumRedirection 8
$bytes = [System.IO.File]::ReadAllBytes($OutputPath)
if ($OutputPath.ToLowerInvariant().EndsWith(".pdf")) {
    $signature = [System.Text.Encoding]::ASCII.GetString($bytes, 0, [Math]::Min(5, $bytes.Length))
    if ($signature -ne "%PDF-") {
        Remove-Item -LiteralPath $OutputPath -Force
        throw "Downloaded content is not a valid PDF"
    }
}

$hash = (Get-FileHash -LiteralPath $OutputPath -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Output "DOWNLOAD_OK SHA256=$hash PATH=$OutputPath"
