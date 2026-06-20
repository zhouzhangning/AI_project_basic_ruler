param(
    [string]$ProjectPath,
    [switch]$InstallCli,
    [switch]$ConfigureAgents,
    [switch]$InitProject,
    [switch]$EnsureGitIgnore,
    [switch]$DisableTelemetry
)

$ErrorActionPreference = "Stop"

function Test-CommandExists([string]$Name) {
    return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
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

if ($InstallCli) {
    if (Test-CommandExists "codegraph") {
        Write-Host "codegraph is already available."
    } elseif (Test-CommandExists "npm") {
        Write-Host "Installing CodeGraph CLI with npm..."
        npm install -g @colbymchenry/codegraph
    } else {
        throw "codegraph and npm are not available. Install Node.js/npm or install CodeGraph manually first."
    }
}

if (-not (Test-CommandExists "codegraph")) {
    Write-Host "codegraph is not available on PATH."
    Write-Host "Run with -InstallCli, or install it manually, then open a new terminal."
    exit 0
}

Write-Host "CodeGraph version:"
codegraph version

if ($DisableTelemetry) {
    Write-Host "Disabling CodeGraph telemetry..."
    codegraph telemetry off
}

if ($ConfigureAgents) {
    Write-Host "Configuring detected AI agents..."
    codegraph install
}

if ($ProjectPath) {
    $resolvedProject = (Resolve-Path -LiteralPath $ProjectPath).Path

    if ($EnsureGitIgnore) {
        Add-CodeGraphGitIgnore $resolvedProject
    }

    if ($InitProject) {
        Write-Host "Initializing CodeGraph project index..."
        codegraph init $resolvedProject
    }

    Write-Host "Project CodeGraph status:"
    codegraph status $resolvedProject
}

if (-not $InstallCli -and -not $ConfigureAgents -and -not $InitProject -and -not $EnsureGitIgnore -and -not $DisableTelemetry) {
    Write-Host "No action flags were provided. This run only checked CodeGraph availability."
    Write-Host "Use -InstallCli, -ConfigureAgents, -InitProject, -EnsureGitIgnore, or -DisableTelemetry to make changes."
}
