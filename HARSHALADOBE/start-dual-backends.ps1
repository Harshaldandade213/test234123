Write-Host "Starting Dual Backend System..." -ForegroundColor Green
Write-Host ""

Write-Host "[1/4] Installing adobev4 dependencies..." -ForegroundColor Yellow
Set-Location ..\adobev4
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install adobev4 dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[2/4] Starting adobev4 backend (port 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python main.py" -WindowStyle Normal
Start-Sleep -Seconds 3

Write-Host "[3/4] Installing HARSHALADOBE backend dependencies..." -ForegroundColor Yellow
Set-Location backend
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install HARSHALADOBE backend dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[4/4] Starting HARSHALADOBE backend (port 8001)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python main.py" -WindowStyle Normal
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Dual Backend System started successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "AdobeV4 Backend: http://localhost:8000" -ForegroundColor White
Write-Host "HARSHALADOBE Backend: http://localhost:8001" -ForegroundColor White
Write-Host "AdobeV4 API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "HARSHALADOBE API Docs: http://localhost:8001/docs" -ForegroundColor White
Write-Host ""
Write-Host "Press Enter to close this window..." -ForegroundColor Yellow
Read-Host
