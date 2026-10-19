param(
    [string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = "Stop"

function New-ZipArchive {
    param(
        [Parameter(Mandatory = $true)]
        [string]$SourceDirectory,
        [Parameter(Mandatory = $true)]
        [string]$DestinationPath
    )

    $zipBuilder = Join-Path $PSScriptRoot "create_zip.py"
    & python $zipBuilder $SourceDirectory $DestinationPath
    if ($LASTEXITCODE -ne 0) {
        throw "Unable to create archive: $DestinationPath"
    }
}

$resolvedProject = [System.IO.Path]::GetFullPath($ProjectRoot)
$stageRoot = [System.IO.Path]::GetFullPath((Join-Path $resolvedProject "tmp\package-stage"))
$distRoot = [System.IO.Path]::GetFullPath((Join-Path $resolvedProject "dist"))

if (-not $stageRoot.StartsWith($resolvedProject, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Unsafe staging path"
}
if (-not $distRoot.StartsWith($resolvedProject, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Unsafe output path"
}

if (Test-Path -LiteralPath $stageRoot) {
    Remove-Item -LiteralPath $stageRoot -Recurse -Force
}
New-Item -ItemType Directory -Path $stageRoot -Force | Out-Null
New-Item -ItemType Directory -Path $distRoot -Force | Out-Null

$knowledge = Join-Path $resolvedProject "TOR_EXPERT_CURRENT_KNOWLEDGE"
$skill = Join-Path $resolvedProject "skills\tor-government-expert"
$license = Join-Path $resolvedProject "LICENSE"
$thirdPartyNotices = Join-Path $resolvedProject "THIRD_PARTY_NOTICES.md"

$knowledgeZip = Join-Path $distRoot "TOR_EXPERT_CURRENT_KNOWLEDGE.zip"
$pluginZip = Join-Path $distRoot "tor-government-expert-chatgpt-plugin.zip"
$geminiZip = Join-Path $distRoot "tor-government-expert-gemini-skill.zip"

foreach ($zip in @($knowledgeZip, $pluginZip, $geminiZip)) {
    if (Test-Path -LiteralPath $zip) {
        Remove-Item -LiteralPath $zip -Force
    }
}

$knowledgeStage = Join-Path $stageRoot "knowledge"
New-Item -ItemType Directory -Path $knowledgeStage -Force | Out-Null
Copy-Item -LiteralPath $knowledge -Destination $knowledgeStage -Recurse
Copy-Item -LiteralPath $license, $thirdPartyNotices -Destination $knowledgeStage
New-ZipArchive -SourceDirectory $knowledgeStage -DestinationPath $knowledgeZip

$pluginStage = Join-Path $stageRoot "chatgpt-plugin"
New-Item -ItemType Directory -Path $pluginStage -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $resolvedProject "plugin.json") -Destination $pluginStage
Copy-Item -LiteralPath $license, $thirdPartyNotices -Destination $pluginStage
Copy-Item -LiteralPath $skill -Destination (Join-Path $pluginStage "skills\tor-government-expert") -Recurse
Copy-Item -LiteralPath $knowledge -Destination (Join-Path $pluginStage "TOR_EXPERT_CURRENT_KNOWLEDGE") -Recurse
New-ZipArchive -SourceDirectory $pluginStage -DestinationPath $pluginZip

$geminiStage = Join-Path $stageRoot "gemini-skill"
$geminiSkill = Join-Path $geminiStage ".gemini\skills\tor-government-expert"
New-Item -ItemType Directory -Path $geminiSkill -Force | Out-Null
Copy-Item -Path (Join-Path $skill "*") -Destination $geminiSkill -Recurse
$knowledgeTarget = Join-Path $geminiSkill "references\knowledge\TOR_EXPERT_CURRENT_KNOWLEDGE"
New-Item -ItemType Directory -Path (Split-Path -Parent $knowledgeTarget) -Force | Out-Null
Copy-Item -LiteralPath $knowledge -Destination $knowledgeTarget -Recurse
Copy-Item -LiteralPath (Join-Path $resolvedProject "README.md") -Destination $geminiStage
Copy-Item -LiteralPath $license, $thirdPartyNotices -Destination $geminiStage
New-ZipArchive -SourceDirectory $geminiStage -DestinationPath $geminiZip

Write-Output "PACKAGE_BUILD_OK"
Get-Item $knowledgeZip, $pluginZip, $geminiZip | Select-Object Name, Length
