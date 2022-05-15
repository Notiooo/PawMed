@echo off
cls
set /p name=Give me your database name: 
echo DATABASE_NAME=%name% > "..\PawMed\.env"
set /p host=Give me your database host: 
echo DATABASE_HOST=%host% >> "..\PawMed\.env"
set /p port=Give me your database port: 
echo DATABASE_PORT=%port% >> "..\PawMed\.env"
set /p user=Give me your database user: 
echo DATABASE_USER=%user% >> "..\PawMed\.env"
set /p password=Give me your database password: 
echo DATABASE_PASSWORD=%password% >> "..\PawMed\.env"
exit