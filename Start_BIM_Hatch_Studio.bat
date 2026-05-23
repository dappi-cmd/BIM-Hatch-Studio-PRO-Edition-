@echo off
echo ===================================================
echo        Starting BIM Hatch Studio Servers...
echo ===================================================

cd /d "%~dp0"

echo [1/3] Starting Python AI Engine (Port 8000)...
start "Python AI Engine" cmd /c "cd python-ai-engine && venv\Scripts\activate && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

echo [2/3] Starting Node.js Backend (Port 5000)...
start "Node.js Backend" cmd /c "cd backend && npm run dev"

echo [3/3] Starting Next.js Frontend UI (Port 3000)...
start "Next.js Frontend" cmd /c "cd frontend && npm run dev"

echo.
echo All services are starting up in separate windows.
echo Waiting 10 seconds for servers to boot up before opening the UI...
timeout /t 10

echo Opening Web UI...
start http://localhost:3000

echo Done! You can close this window.
exit
