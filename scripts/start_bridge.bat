@echo off
title Mobbin Web Ingestion Bridge
echo Starting Web Ingestion Bridge on http://127.0.0.1:3848...
python "%~dp0ingest_bridge.py"
pause
