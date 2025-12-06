# Start Backend
Write-Host "Starting Backend..." -ForegroundColor Green
Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "& { . .\.venv\Scripts\Activate.ps1; cd backend; python -m app.main }"

# Start Frontend
Write-Host "Starting Frontend..." -ForegroundColor Green
Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "& { cd frontend; npm run dev }"

Write-Host "App is starting! Check the opened windows." -ForegroundColor Cyan
