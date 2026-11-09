@echo off
setlocal
if exist "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" (
  "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" "%~dp0preview.py" --port 4333
) else (
  python "%~dp0preview.py" --port 4333
)
if errorlevel 1 pause
