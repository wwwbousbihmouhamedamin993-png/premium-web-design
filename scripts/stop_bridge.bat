@echo off
title Stop Web Ingestion Bridge
echo Stopping Web Ingestion Bridge on port 3848...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3848 ^| findstr LISTENING') do (
    taskkill /f /pid %%a >nul 2>&1
    echo Terminated process %%a
)
echo Web Ingestion Bridge stopped.
pause
