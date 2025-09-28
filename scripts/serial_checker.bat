@echo off
setlocal EnableExtensions EnableDelayedExpansion
title Odczyt nr seryjnego PC/BIOS
chcp 65001 >nul

echo.
echo === TestVarment Mod2 Odczyt nr seryjnego PC/BIOS ===
echo.
set "PCNAME="
set /p PCNAME=Podaj nazwę komputera (użyta w nazwach plików) ^> 

REM Jeżeli użytkownik nic nie wpisze, użyj aktualnej nazwy komputera
if "%PCNAME%"=="" set "PCNAME=%COMPUTERNAME%"

REM Ścieżka do Pulpitu
set "DESKTOP=%USERPROFILE%\Desktop"

echo.
echo Pobieram numer seryjny BIOS/laptopa...

REM Pobierz numer seryjny BIOS (PowerShell/CIM), fallback na WMIC
set "BIOS_SN="
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "(Get-CimInstance Win32_BIOS).SerialNumber"`) do set "BIOS_SN=%%A"

if not defined BIOS_SN (
  for /f "usebackq skip=1 delims=" %%A in (`wmic bios get serialnumber`) do (
    if not defined BIOS_SN set "BIOS_SN=%%A"
  )
)

REM Oczyść z ewentualnych spacji/braków linii
if defined BIOS_SN (
  for /f "tokens=* delims= " %%A in ("%BIOS_SN%") do set "BIOS_SN=%%A"
) else (
  set "BIOS_SN=Nie wykryto numeru seryjnego (brak uprawnień/sterowniki/WMI?)"
)

> "%DESKTOP%\%PCNAME%_serial.txt" echo %BIOS_SN%
echo  -> Zapisano do "%DESKTOP%\%PCNAME%_serial.txt"

echo.
endlocal
