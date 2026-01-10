# PowerShell script to fix SEO content issues

Write-Host "SEO Content Optimization Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

$allPages = Get-ChildItem -Path "." -Include "*.html" -Recurse -Exclude "_site" | 
            Where-Object { $_.DirectoryName -notlike "*_site*" -and $_.DirectoryName -notlike "*node_modules*" }

$stats = @{
    TotalPages = 0
    TitlesFixed = 0
    DescriptionsFixed = 0
    LinksFixed = 0
}

foreach ($page in $allPages) {
    $stats.TotalPages++
    $content = Get-Content $page.FullName -Raw
    $modified = $false
    
    Write-Host "Processing: $($page.Name)"
    
    # Fix page titles over 60 characters
    if ($content -match '<title>([^<]{61,})</title>') {
        $oldTitle = $matches[1]
        $newTitle = $oldTitle.Substring(0, 57) + "..."
        $content = $content -replace [regex]::Escape("<title>$oldTitle</title>"), "<title>$newTitle</title>"
        Write-Host "  - Shortened page title" -ForegroundColor Green
        $stats.TitlesFixed++
        $modified = $true
    }
    
    # Fix meta descriptions over 155 characters
    $descPattern = '<meta\s+content="([^"]{156,})"\s+name="description"'
    if ($content -match $descPattern) {
        $oldDesc = $matches[1]
        $newDesc = $oldDesc.Substring(0, 152) + "..."
        $content = $content -replace [regex]::Escape($oldDesc), $newDesc
        Write-Host "  - Shortened meta description" -ForegroundColor Green
        $stats.DescriptionsFixed++
        $modified = $true
    }
    
    # Add rel="noopener" to external links with target="_blank"
    $linkPattern = 'target="_blank"(?!\s+rel="[^"]*noopener)'
    if ($content -match $linkPattern) {
        $content = $content -replace 'target="_blank"', 'target="_blank" rel="noopener"'
        Write-Host "  - Added rel=noopener to external links" -ForegroundColor Green
        $stats.LinksFixed++
        $modified = $true
    }
    
    if ($modified) {
        Set-Content -Path $page.FullName -Value $content -NoNewline
    }
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "  Total pages processed: $($stats.TotalPages)" -ForegroundColor White
Write-Host "  Titles fixed: $($stats.TitlesFixed)" -ForegroundColor Green
Write-Host "  Descriptions fixed: $($stats.DescriptionsFixed)" -ForegroundColor Green
Write-Host "  Links fixed: $($stats.LinksFixed)" -ForegroundColor Green
Write-Host ""
Write-Host "SEO content optimization completed!" -ForegroundColor Cyan