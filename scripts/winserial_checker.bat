@echo off
setlocal EnableExtensions EnableDelayedExpansion
title Odczyt klucza produktu Windows
chcp 65001 >nul

echo.
echo === TestVarment Mod3 Odczyt klucza produktu Windows ===
echo.
set "PCNAME="
set /p PCNAME=Podaj nazwę komputera (użyta w nazwach plików) ^> 

REM Jeżeli użytkownik nic nie wpisze, użyj aktualnej nazwy komputera
if "%PCNAME%"=="" set "PCNAME=%COMPUTERNAME%"

REM Ścieżka do Pulpitu
set "DESKTOP=%USERPROFILE%\Desktop"

echo.
echo Pobieram klucz produktu Windows...

REM Spróbuj odczytać klucz OEM (OA3x) lub BackupProductKeyDefault z rejestru
set "WIN_KEY="
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "$k=(Get-CimInstance -Query 'select * from SoftwareLicensingService').OA3xOriginalProductKey; if([string]::IsNullOrWhiteSpace($k)){ try{(Get-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SoftwareProtectionPlatform' -Name BackupProductKeyDefault -ErrorAction Stop).BackupProductKeyDefault}catch{''} } else {$k}"`) do set "WIN_KEY=%%A"

REM Oczyszczenie białych znaków z wyniku (bez wyciszania błędów)
if defined WIN_KEY for /f "tokens=* delims= " %%A in ("%WIN_KEY%") do set "WIN_KEY=%%A"

if not defined WIN_KEY set "WIN_KEY=Brak klucza OEM/backup -> możliwy klucz cyfrowy przypisany do konta Microsoft."

> "%DESKTOP%\%PCNAME%_Win_serial.txt" echo %WIN_KEY%
echo  -> Zapisano do "%DESKTOP%\%PCNAME%_Win_serial.txt"

echo.
endlocal
