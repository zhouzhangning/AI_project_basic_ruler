param(
    [string]$RootPath = (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)),
    [int]$MaxMainRuleLines = 180,
    [int]$MaxDocLines = 260,
    [int]$MaxPromptLines = 120
)

$ErrorActionPreference = "Stop"

$root = (Resolve-Path -LiteralPath $RootPath).Path
$failures = New-Object System.Collections.Generic.List[string]
$warnings = New-Object System.Collections.Generic.List[string]

function Add-Failure([string]$message) {
    $script:failures.Add($message) | Out-Null
}

function Add-Warning([string]$message) {
    $script:warnings.Add($message) | Out-Null
}

function Test-RequiredFile([string]$relativePath) {
    $path = Join-Path $root $relativePath
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        Add-Failure "Missing required file: $relativePath"
    }
}

function Test-LineLimit([string]$relativePath, [int]$limit) {
    $path = Join-Path $root $relativePath
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        return
    }

    $lineCount = (Get-Content -LiteralPath $path -Encoding UTF8 | Measure-Object -Line).Lines
    if ($lineCount -gt $limit) {
        Add-Warning "$relativePath has $lineCount lines; suggested limit is $limit."
    }
}

$requiredFiles = @(
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    ".cursorrules",
    "README-AI.md",
    "docs\ai-approval-rules.md",
    "docs\ai-task-template.md",
    "docs\ai-work-log.md",
    "docs\codegraph-integration.md",
    "docs\feature-inventory.md",
    "docs\project-memory.md",
    "docs\evolution-rules.md",
    "docs\sync-rules.md",
    "docs\maintenance-checklist.md",
    "docs\release-checklist.md",
    "docs\test-checklist.md",
    "scripts\init-ai-dev-system.ps1",
    "scripts\update-ai-dev-system.ps1",
    "scripts\sync-selected-ai-dev-system.ps1",
    "scripts\start-ai-dev-system-gui.ps1",
    "scripts\audit-ai-dev-system.ps1",
    "scripts\setup-codegraph.ps1",
    "start-ai-dev-system-gui.bat"
)

foreach ($file in $requiredFiles) {
    Test-RequiredFile $file
}

Test-LineLimit "AGENTS.md" $MaxMainRuleLines
Test-LineLimit "CLAUDE.md" $MaxPromptLines
Test-LineLimit "GEMINI.md" $MaxPromptLines
Test-LineLimit "README-AI.md" $MaxPromptLines

Get-ChildItem -LiteralPath (Join-Path $root "docs") -Filter "*.md" -File -ErrorAction SilentlyContinue | ForEach-Object {
    Test-LineLimit ("docs\" + $_.Name) $MaxDocLines
}

Get-ChildItem -LiteralPath (Join-Path $root "prompts") -Filter "*.md" -File -ErrorAction SilentlyContinue | ForEach-Object {
    Test-LineLimit ("prompts\" + $_.Name) $MaxPromptLines
}

$readme = Join-Path $root "README.md"
if (Test-Path -LiteralPath $readme) {
    $readmeText = Get-Content -LiteralPath $readme -Raw -Encoding UTF8
    foreach ($file in $requiredFiles) {
        $name = Split-Path -Leaf $file
        if ($name -eq "README.md") {
            continue
        }
        if ($readmeText -notmatch [regex]::Escape($name)) {
            Add-Warning "README.md may not mention: $name"
        }
    }
}

Write-Host "AI Dev System audit"
Write-Host "Root: $root"
Write-Host ""

if ($warnings.Count -gt 0) {
    Write-Host "Warnings:"
    foreach ($warning in $warnings) {
        Write-Host " - $warning"
    }
    Write-Host ""
}

if ($failures.Count -gt 0) {
    Write-Host "Failures:"
    foreach ($failure in $failures) {
        Write-Host " - $failure"
    }
    exit 1
}

Write-Host "Audit passed."
