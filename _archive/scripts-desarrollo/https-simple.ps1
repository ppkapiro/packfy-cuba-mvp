# Solucion rapida: Usar ngrok para HTTPS
Write-Host "SOLUCION RAPIDA: NGROK PARA HTTPS" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green

Write-Host "1. Descargando ngrok..." -ForegroundColor Yellow

# Descargar ngrok
$ngrokUrl = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
$ngrokZip = "ngrok.zip"
$ngrokDir = "ngrok"

if (!(Test-Path $ngrokDir)) {
    Write-Host "Descargando ngrok..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $ngrokUrl -OutFile $ngrokZip
    Expand-Archive -Path $ngrokZip -DestinationPath $ngrokDir -Force
    Remove-Item $ngrokZip
    Write-Host "ngrok descargado" -ForegroundColor Green
} else {
    Write-Host "ngrok ya esta disponible" -ForegroundColor Green
}

Write-Host "`n2. Iniciando tunnel HTTPS..." -ForegroundColor Yellow
Write-Host "MANTEN ESTA VENTANA ABIERTA" -ForegroundColor Red

# Iniciar ngrok
Start-Process -FilePath ".\ngrok\ngrok.exe" -ArgumentList "http", "5173"

Write-Host "`n3. COMO OBTENER LA URL HTTPS:" -ForegroundColor Yellow
Write-Host "1. Se abrio una ventana de ngrok" -ForegroundColor White
Write-Host "2. Busca la linea que dice 'Forwarding'" -ForegroundColor White
Write-Host "3. Copia la URL que empieza con 'https://'" -ForegroundColor White
Write-Host "4. Esa URL funcionara en cualquier dispositivo" -ForegroundColor White

Write-Host "`nTambien puedes ver las URLs en:" -ForegroundColor Yellow
Write-Host "http://localhost:4040" -ForegroundColor Cyan

Write-Host "`nConfiguracion completada!" -ForegroundColor Green
