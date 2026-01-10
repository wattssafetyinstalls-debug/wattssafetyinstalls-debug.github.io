# PowerShell script to fix canonical tag issues in service pages

Write-Host "Canonical Tag Fix Script" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan
Write-Host ""

$servicePages = Get-ChildItem -Path "./services" -Recurse -Filter "index.html"
$stats = @{
    TotalPages = 0
    Fixed = 0
    Errors = 0
}

foreach ($page in $servicePages) {
    $stats.TotalPages++
    
    try {
        Write-Host "Processing: $($page.Directory.Name)" -NoNewline
        
        $content = Get-Content $page.FullName -Raw
        $originalContent = $content
        
        # Extract service slug from path
        $servicePath = $page.Directory.Name
        $canonicalUrl = "https://wattsatpcontractor.com/services/$servicePath/"
        
        # Count existing canonicals
        $pattern = '<link[^>]*rel="canonical"[^>]*>'
        $canonicalCount = ([regex]::Matches($content, $pattern)).Count
        
        if ($canonicalCount -gt 1) {
            Write-Host " - Found $canonicalCount canonicals" -ForegroundColor Yellow
        }
        
        # Remove all existing canonical tags
        $content = $content -replace '<link\s+href="[^"]*"\s+rel="canonical"\s*/?>', ''
        $content = $content -replace '<link\s+rel="canonical"\s+href="[^"]*"\s*/?>', ''
        
        # Create new canonical tag
        $newCanonical = '<link href="' + $canonicalUrl + '" rel="canonical"/>'
        
        # Find the position right after meta description
        if ($content -match '(<meta[^>]*name="description"[^>]*>)') {
            $content = $content -replace '(<meta[^>]*name="description"[^>]*>)', ('$1' + $newCanonical)
        }
        elseif ($content -match '(<meta[^>]*charset[^>]*>)') {
            $content = $content -replace '(<meta[^>]*charset[^>]*>)', ('$1' + $newCanonical)
        }
        else {
            $content = $content -replace '(<head>)', ('$1' + "`n" + $newCanonical)
        }
        
        # Only save if content changed
        if ($content -ne $originalContent) {
            Set-Content -Path $page.FullName -Value $content -NoNewline
            Write-Host " - Fixed" -ForegroundColor Green
            $stats.Fixed++
        }
        else {
            Write-Host " - Already correct" -ForegroundColor Gray
        }
    }
    catch {
        Write-Host " - Error: $($_.Exception.Message)" -ForegroundColor Red
        $stats.Errors++
    }
}

Write-Host ""
Write-Host "========================" -ForegroundColor Cyan
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "  Total pages: $($stats.TotalPages)" -ForegroundColor White
Write-Host "  Fixed: $($stats.Fixed)" -ForegroundColor Green
Write-Host "  Errors: $($stats.Errors)" -ForegroundColor Red
Write-Host ""
Write-Host "Canonical fix completed!" -ForegroundColor Cyan