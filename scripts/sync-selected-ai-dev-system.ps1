param(
    [Parameter(Mandatory = $true)]
    [string]$TargetPath,

    [string[]]$Features,

    [switch]$Overwrite,
    [switch]$EnsureCodeGraphGitIgnore,
    [switch]$ListFeatures
)

$ErrorActionPreference = "Stop"

$sourceRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

$featureMap = [ordered]@{
    "core-rules" = @{
        Name = "AI collaboration rules"
        Items = @("AGENTS.md", "CLAUDE.md", "GEMINI.md", ".cursorrules", "README-AI.md")
    }
    "approval" = @{
        Name = "approval and risk boundaries"
        Items = @("docs\ai-approval-rules.md")
    }
    "task-prompts" = @{
        Name = "task prompts"
        Items = @("prompts")
    }
    "memory" = @{
        Name = "project memory and work logs"
        Items = @("docs\project-memory.md", "docs\ai-work-log.md", "docs\ai-task-template.md")
    }
    "maintenance" = @{
        Name = "audit and maintenance"
        Items = @(
            "docs\evolution-rules.md",
            "docs\maintenance-checklist.md",
            "docs\feature-inventory.md",
            "scripts\audit-ai-dev-system.ps1"
        )
    }
    "sync-tools" = @{
        Name = "init and sync tools"
        Items = @(
            "docs\sync-rules.md",
            "scripts\init-ai-dev-system.ps1",
            "scripts\update-ai-dev-system.ps1",
            "scripts\sync-selected-ai-dev-system.ps1",
            "scripts\start-ai-dev-system-gui.ps1"
        )
    }
    "codegraph" = @{
        Name = "optional CodeGraph infrastructure"
        Items = @("docs\codegraph-integration.md", "scripts\setup-codegraph.ps1")
    }
    "release-test" = @{
        Name = "release and test checklists"
        Items = @("docs\release-checklist.md", "docs\test-checklist.md")
    }
}

function Show-Features {
    Write-Host "Available features:"
    foreach ($key in $featureMap.Keys) {
        Write-Host (" - {0}: {1}" -f $key, $featureMap[$key].Name)
    }
}

function Add-CodeGraphGitIgnore([string]$Root) {
    $gitignore = Join-Path $Root ".gitignore"
    if (-not (Test-Path -LiteralPath $gitignore)) {
        New-Item -ItemType File -Path $gitignore | Out-Null
    }

    $content = Get-Content -LiteralPath $gitignore -Raw -Encoding UTF8
    if ($content -notmatch "(?m)^\.codegraph/$") {
        Add-Content -LiteralPath $gitignore -Encoding UTF8 -Value "`n# Local CodeGraph index`n.codegraph/"
        Write-Host "Added .codegraph/ to .gitignore"
    } else {
        Write-Host ".gitignore already contains .codegraph/"
    }
}

function Copy-TemplateItem([string]$RelativePath, [string]$TargetRoot) {
    $source = Join-Path $sourceRoot $RelativePath
    $target = Join-Path $TargetRoot $RelativePath

    if (-not (Test-Path -LiteralPath $source)) {
        Write-Host "Skip missing source: $RelativePath"
        return
    }

    $targetParent = Split-Path -Parent $target
    if (-not (Test-Path -LiteralPath $targetParent)) {
        New-Item -ItemType Directory -Force -Path $targetParent | Out-Null
    }

    if (Test-Path -LiteralPath $target) {
        if (-not $Overwrite) {
            Write-Host "Skip existing: $RelativePath"
            return
        }
        Remove-Item -LiteralPath $target -Recurse -Force
    }

    Copy-Item -LiteralPath $source -Destination $target -Recurse -Force
    Write-Host "Synced: $RelativePath"
}

if ($ListFeatures) {
    Show-Features
    exit 0
}

$normalizedFeatures = @()
foreach ($featureValue in $Features) {
    foreach ($part in ($featureValue -split ",")) {
        $trimmed = $part.Trim()
        if ($trimmed) {
            $normalizedFeatures += $trimmed
        }
    }
}

if (-not $normalizedFeatures -or $normalizedFeatures.Count -eq 0) {
    throw "No features selected. Use -ListFeatures to see available feature ids."
}

$targetRoot = (Resolve-Path -LiteralPath $TargetPath).Path
$selectedItems = New-Object System.Collections.Generic.List[string]

foreach ($feature in $normalizedFeatures) {
    if (-not $featureMap.Contains($feature)) {
        throw "Unknown feature: $feature"
    }

    Write-Host ("Feature: {0} ({1})" -f $featureMap[$feature].Name, $feature)
    foreach ($item in $featureMap[$feature].Items) {
        if (-not $selectedItems.Contains($item)) {
            $selectedItems.Add($item) | Out-Null
        }
    }
}

foreach ($item in $selectedItems) {
    Copy-TemplateItem $item $targetRoot
}

if ($EnsureCodeGraphGitIgnore -or $normalizedFeatures -contains "codegraph") {
    Add-CodeGraphGitIgnore $targetRoot
}

Write-Host "Selected AI dev system sync completed in $targetRoot"
