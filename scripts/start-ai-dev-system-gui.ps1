$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$syncScript = Join-Path $scriptRoot "sync-selected-ai-dev-system.ps1"

$featureDefinitions = @(
    @{ Id = "core-rules"; Label = "AI collaboration rules"; Checked = $true },
    @{ Id = "approval"; Label = "Approval and risk boundaries"; Checked = $true },
    @{ Id = "task-prompts"; Label = "Task prompts"; Checked = $true },
    @{ Id = "memory"; Label = "Project memory and work logs"; Checked = $true },
    @{ Id = "maintenance"; Label = "Audit and maintenance"; Checked = $true },
    @{ Id = "sync-tools"; Label = "Init and sync tools"; Checked = $true },
    @{ Id = "codegraph"; Label = "Optional CodeGraph infrastructure"; Checked = $false },
    @{ Id = "release-test"; Label = "Release and test checklists"; Checked = $true }
)

$form = New-Object System.Windows.Forms.Form
$form.Text = "AI Dev System Sync"
$form.StartPosition = "CenterScreen"
$form.Size = New-Object System.Drawing.Size(720, 620)
$form.MinimumSize = New-Object System.Drawing.Size(680, 560)

$targetLabel = New-Object System.Windows.Forms.Label
$targetLabel.Text = "Target project"
$targetLabel.Location = New-Object System.Drawing.Point(16, 18)
$targetLabel.Size = New-Object System.Drawing.Size(120, 24)
$form.Controls.Add($targetLabel)

$targetBox = New-Object System.Windows.Forms.TextBox
$targetBox.Location = New-Object System.Drawing.Point(16, 44)
$targetBox.Size = New-Object System.Drawing.Size(560, 26)
$form.Controls.Add($targetBox)

$browseButton = New-Object System.Windows.Forms.Button
$browseButton.Text = "Browse..."
$browseButton.Location = New-Object System.Drawing.Point(586, 42)
$browseButton.Size = New-Object System.Drawing.Size(92, 30)
$form.Controls.Add($browseButton)

$group = New-Object System.Windows.Forms.GroupBox
$group.Text = "Select features"
$group.Location = New-Object System.Drawing.Point(16, 88)
$group.Size = New-Object System.Drawing.Size(662, 225)
$form.Controls.Add($group)

$checkboxes = @{}
$y = 26
foreach ($feature in $featureDefinitions) {
    $checkbox = New-Object System.Windows.Forms.CheckBox
    $checkbox.Text = $feature.Label
    $checkbox.Tag = $feature.Id
    $checkbox.Checked = [bool]$feature.Checked
    $checkbox.Location = New-Object System.Drawing.Point(18, $y)
    $checkbox.Size = New-Object System.Drawing.Size(310, 24)
    $group.Controls.Add($checkbox)
    $checkboxes[$feature.Id] = $checkbox
    $y += 24
}

$overwriteBox = New-Object System.Windows.Forms.CheckBox
$overwriteBox.Text = "Overwrite existing files"
$overwriteBox.Location = New-Object System.Drawing.Point(360, 28)
$overwriteBox.Size = New-Object System.Drawing.Size(250, 24)
$group.Controls.Add($overwriteBox)

$codegraphIgnoreBox = New-Object System.Windows.Forms.CheckBox
$codegraphIgnoreBox.Text = "Add .codegraph/ to target .gitignore"
$codegraphIgnoreBox.Checked = $true
$codegraphIgnoreBox.Location = New-Object System.Drawing.Point(360, 58)
$codegraphIgnoreBox.Size = New-Object System.Drawing.Size(280, 24)
$group.Controls.Add($codegraphIgnoreBox)

$selectAllButton = New-Object System.Windows.Forms.Button
$selectAllButton.Text = "Select all"
$selectAllButton.Location = New-Object System.Drawing.Point(360, 98)
$selectAllButton.Size = New-Object System.Drawing.Size(88, 30)
$group.Controls.Add($selectAllButton)

$clearButton = New-Object System.Windows.Forms.Button
$clearButton.Text = "Clear"
$clearButton.Location = New-Object System.Drawing.Point(458, 98)
$clearButton.Size = New-Object System.Drawing.Size(88, 30)
$group.Controls.Add($clearButton)

$runButton = New-Object System.Windows.Forms.Button
$runButton.Text = "Sync"
$runButton.Location = New-Object System.Drawing.Point(16, 326)
$runButton.Size = New-Object System.Drawing.Size(120, 34)
$form.Controls.Add($runButton)

$statusLabel = New-Object System.Windows.Forms.Label
$statusLabel.Text = "Idle"
$statusLabel.Location = New-Object System.Drawing.Point(150, 334)
$statusLabel.Size = New-Object System.Drawing.Size(520, 24)
$form.Controls.Add($statusLabel)

$outputBox = New-Object System.Windows.Forms.TextBox
$outputBox.Location = New-Object System.Drawing.Point(16, 376)
$outputBox.Size = New-Object System.Drawing.Size(662, 170)
$outputBox.Multiline = $true
$outputBox.ScrollBars = "Vertical"
$outputBox.ReadOnly = $true
$outputBox.Font = New-Object System.Drawing.Font("Consolas", 9)
$form.Controls.Add($outputBox)

$browseButton.Add_Click({
    $dialog = New-Object System.Windows.Forms.FolderBrowserDialog
    $dialog.Description = "Select target project folder"
    if ($dialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        $targetBox.Text = $dialog.SelectedPath
    }
})

$selectAllButton.Add_Click({
    foreach ($checkbox in $checkboxes.Values) {
        $checkbox.Checked = $true
    }
})

$clearButton.Add_Click({
    foreach ($checkbox in $checkboxes.Values) {
        $checkbox.Checked = $false
    }
})

$runButton.Add_Click({
    try {
        $outputBox.Clear()
        $targetPath = $targetBox.Text.Trim()
        if (-not $targetPath) {
            throw "Select a target project folder."
        }
        if (-not (Test-Path -LiteralPath $targetPath -PathType Container)) {
            throw "Target project folder does not exist: $targetPath"
        }

        $features = @()
        foreach ($checkbox in $checkboxes.Values) {
            if ($checkbox.Checked) {
                $features += [string]$checkbox.Tag
            }
        }
        if ($features.Count -eq 0) {
            throw "Select at least one feature."
        }

        $statusLabel.Text = "Syncing..."
        $form.Refresh()

        $args = @("-TargetPath", $targetPath, "-Features")
        $args += $features
        if ($overwriteBox.Checked) {
            $args += "-Overwrite"
        }
        if ($codegraphIgnoreBox.Checked) {
            $args += "-EnsureCodeGraphGitIgnore"
        }

        $result = & $syncScript @args 2>&1 | Out-String
        $outputBox.Text = $result
        $statusLabel.Text = "Done"
    } catch {
        $outputBox.Text = $_.Exception.Message
        $statusLabel.Text = "Failed"
    }
})

[void]$form.ShowDialog()
