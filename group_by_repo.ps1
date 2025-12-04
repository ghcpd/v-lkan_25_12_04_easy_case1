$src = Join-Path $PSScriptRoot 'repo_metadata.jsonl'
if (-not (Test-Path $src)) { Write-Error "Source file not found: $src"; exit 1 }
Get-Content $src | ForEach-Object -Begin {$i=0} -Process {
    $i++
    $line = $_
    if ([string]::IsNullOrWhiteSpace($line)) { return }
    try {
        $obj = ConvertFrom-Json $line -ErrorAction Stop
    } catch {
        Write-Warning "Failed to parse JSON on line $i: $_"
        return
    }
    if (-not $obj.repo) { Write-Warning "No repo field on line $i"; return }
    $folder = $obj.repo -replace '/', '__'
    $outdir = Join-Path $PSScriptRoot $folder
    if (-not (Test-Path $outdir)) { New-Item -ItemType Directory -Path $outdir | Out-Null }
    $outfile = Join-Path $outdir 'records.jsonl'
    Add-Content -Path $outfile -Value $line -Encoding utf8
} ; Write-Host 'Grouping complete'