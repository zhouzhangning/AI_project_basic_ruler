param(
    [string]$CodexHome
)

$ErrorActionPreference = "Stop"

$sourceRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$skillsRoot = Join-Path $sourceRoot "skills"

if (-not $CodexHome) {
    if ($env:CODEX_HOME) {
        $CodexHome = $env:CODEX_HOME
    } else {
        $CodexHome = Join-Path $HOME ".codex"
    }
}

$targetRoot = Join-Path $CodexHome "skills"
New-Item -ItemType Directory -Force -Path $targetRoot | Out-Null

if (-not (Test-Path -LiteralPath $skillsRoot)) {
    Write-Host "No local skills folder found: $skillsRoot"
    exit 0
}

Get-ChildItem -LiteralPath $skillsRoot -Directory | ForEach-Object {
    $target = Join-Path $targetRoot $_.Name
    if (Test-Path -LiteralPath $target) {
        Remove-Item -LiteralPath $target -Recurse -Force
    }
    Copy-Item -LiteralPath $_.FullName -Destination $target -Recurse -Force
    Write-Host "Installed skill: $($_.Name)"
}

Write-Host "Skills installed to $targetRoot"
