Get-ChildItem . -Recurse -Filter "*.html" | Where-Object { $_.Name -ne "404.html" } | ForEach-Object {
    $path = $_.FullName
    $content = Get-Content $path -Raw
    
    # Remove .html from canonicals
    $newContent = $content -replace '(rel="canonical" href="https://wattsatpcontractor\.com/[^"]+)\.html"', '$1"'
    
    if ($newContent -ne $content) {
        Set-Content $path $newContent
        Write-Host "Updated: $path" -ForegroundColor Green
    }
}
