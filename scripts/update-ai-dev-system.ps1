param(
    [Parameter(Mandatory = $true)]
    [string]$TargetPath,

    [switch]$Overwrite,
    [switch]$SkipGitPull
)

$ErrorActionPreference = "Stop"

$sourceRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$targetRoot = (Resolve-Path -LiteralPath $TargetPath).Path

if (-not $SkipGitPull) {
    if (Test-Path -LiteralPath (Join-Path $sourceRoot ".git")) {
        Write-Host "Updating template repository..."
        git -C $sourceRoot pull --ff-only
    }
}

Write-Host "Running template audit..."
& (Join-Path $sourceRoot "scripts\audit-ai-dev-system.ps1") -RootPath $sourceRoot

$items = @(
    "CLAUDE.md",
    "GEMINI.md",
    ".cursorrules",
    "docs\ai-approval-rules.md",
    "docs\ai-task-template.md",
    "docs\codegraph-integration.md",
    "docs\evolution-rules.md",
    "docs\maintenance-checklist.md",
    "docs\release-checklist.md",
    "docs\sync-rules.md",
    "docs\test-checklist.md",
    "prompts",
    "scripts\audit-ai-dev-system.ps1",
    "scripts\sync-selected-ai-dev-system.ps1",
    "scripts\start-ai-dev-system-gui.ps1",
    "start-ai-dev-system-gui.bat",
    "scripts\setup-codegraph.ps1"
)

$preserveByDefault = @(
    "AGENTS.md",
    "README-AI.md",
    "docs\ai-work-log.md",
    "docs\project-memory.md"
)

foreach ($item in $items + $preserveByDefault) {
    $source = Join-Path $sourceRoot $item
    $target = Join-Path $targetRoot $item

    if (-not (Test-Path -LiteralPath $source)) {
        Write-Host "Skip missing source: $item"
        continue
    }

    $targetParent = Split-Path -Parent $target
    if (-not (Test-Path -LiteralPath $targetParent)) {
        New-Item -ItemType Directory -Force -Path $targetParent | Out-Null
    }

    if (Test-Path -LiteralPath $target) {
        if (-not $Overwrite) {
            Write-Host "Skip existing: $item"
            continue
        }
        Remove-Item -LiteralPath $target -Recurse -Force
    }

    Copy-Item -LiteralPath $source -Destination $target -Recurse -Force
    Write-Host "Updated: $item"
}

Write-Host "AI dev system update completed in $targetRoot"
