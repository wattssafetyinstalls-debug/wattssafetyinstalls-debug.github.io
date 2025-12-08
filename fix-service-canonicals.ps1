# PowerShell script to fix all service page canonical URLs
# Run this from the root directory: .\fix-service-canonicals.ps1

Write-Host "Fixing canonical URLs in all service pages..." -ForegroundColor Cyan

# Get all service page index.html files
$servicePages = Get-ChildItem -Path "services" -Filter "index.html" -Recurse

$count = 0
foreach ($file in $servicePages) {
    # Get the service slug from the directory name
    $slug = $file.Directory.Name
    
    # Read the file content
    $content = Get-Content $file.FullName -Raw
    
    # Check current canonical
    if ($content -match 'rel="canonical".*?href="([^"]+)"') {
        $currentCanonical = $matches[1]
        Write-Host "  $slug : $currentCanonical" -ForegroundColor Yellow
    }
    
    # Fix canonical URL - create the correct one
    $correctCanonical = "https://wattsatpcontractor.com/services/$slug/"
    
    # Replace any canonical tag for this service with the correct one
    $pattern = '<link[^>]*rel="canonical"[^>]*href="https://wattsatpcontractor\.com/services/' + [regex]::Escape($slug) + '[^"]*"[^>]*/?>'
    $replacement = '<link rel="canonical" href="' + $correctCanonical + '">'
    
    $newContent = $content -replace $pattern, $replacement
    
    # Write back if changed
    if ($newContent -ne $content) {
        Set-Content -Path $file.FullName -Value $newContent -NoNewline
        Write-Host "    Fixed: $correctCanonical" -ForegroundColor Green
        $count++
    } else {
        Write-Host "    Already correct" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "Fixed $count service page(s)" -ForegroundColor Cyan
Write-Host "Done!" -ForegroundColor Green