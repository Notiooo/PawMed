@echo off
cls
set /p txt=Give me your secret key: 
echo SECRET_KEY=%txt% > "..\PawMed\.env"
exit