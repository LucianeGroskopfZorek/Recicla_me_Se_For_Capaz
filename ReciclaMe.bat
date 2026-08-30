@echo off
cd "C:\Users\Cesar\OneDrive - SENAC-SC\recicla_me"
start python app.py
timeout /t 2
start http://localhost:5000