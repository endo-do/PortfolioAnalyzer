@echo off
SET USER=root
SET DATABASE=portfolioanalyzer

echo Running setup.sql...
mysql -u %USER% -p %DATABASE% < setup.sql

if %ERRORLEVEL% EQU 0 (
    echo DB setup successful!
) else (
    echo DB setup failed!
)

pause