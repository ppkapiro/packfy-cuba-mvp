# Solución rápida: Usar ngrok para HTTPS
Write-Host "🚀 SOLUCIÓN RÁPIDA: NGROK PARA HTTPS" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green

Write-Host "📦 1. Descargando ngrok..." -ForegroundColor Yellow

# Descargar ngrok
$ngrokUrl = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
$ngrokZip = "ngrok.zip"
$ngrokDir = "ngrok"

if (!(Test-Path $ngrokDir)) {
    Write-Host "⬇️ Descargando ngrok..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $ngrokUrl -OutFile $ngrokZip
    Expand-Archive -Path $ngrokZip -DestinationPath $ngrokDir -Force
    Remove-Item $ngrokZip
    Write-Host "✅ ngrok descargado" -ForegroundColor Green
} else {
    Write-Host "✅ ngrok ya está disponible" -ForegroundColor Green
}

Write-Host "`n🌐 2. Iniciando tunnel HTTPS..." -ForegroundColor Yellow
Write-Host "⚠️ MANTÉN ESTA VENTANA ABIERTA" -ForegroundColor Red

# Iniciar ngrok
Start-Process -FilePath ".\ngrok\ngrok.exe" -ArgumentList "http", "5173" -WindowStyle Normal

Write-Host "`n📱 3. CÓMO OBTENER LA URL HTTPS:" -ForegroundColor Yellow
Write-Host "1. Se abrió una ventana de ngrok" -ForegroundColor White
Write-Host "2. Busca la línea que dice 'Forwarding'" -ForegroundColor White
Write-Host "3. Copia la URL que empieza con 'https://'" -ForegroundColor White
Write-Host "4. Esa URL funcionará en cualquier dispositivo" -ForegroundColor White

Write-Host "`n🔍 También puedes ver las URLs en:" -ForegroundColor Yellow
Write-Host "http://localhost:4040" -ForegroundColor Cyan

Write-Host "`nConfiguracion completada!" -ForegroundColor Green
