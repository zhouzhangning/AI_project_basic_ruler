param(
    [Parameter(Mandatory = $true)]
    [string]$TargetPath,

    [switch]$Overwrite
)

$ErrorActionPreference = "Stop"

$sourceRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$targetRoot = (Resolve-Path -LiteralPath $TargetPath).Path

$items = @(
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    ".cursorrules",
    "README-AI.md",
    "docs",
    "prompts",
    "scripts\audit-ai-dev-system.ps1"
)

foreach ($item in $items) {
    $source = Join-Path $sourceRoot $item
    $target = Join-Path $targetRoot $item

    if (Test-Path -LiteralPath $target) {
        if (-not $Overwrite) {
            Write-Host "Skip existing: $target"
            continue
        }
        Remove-Item -LiteralPath $target -Recurse -Force
    }

    Copy-Item -LiteralPath $source -Destination $target -Recurse -Force
    Write-Host "Copied: $item"
}

Write-Host "AI dev system initialized in $targetRoot"
