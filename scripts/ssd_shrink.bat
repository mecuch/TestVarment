@echo off
setlocal EnableExtensions EnableDelayedExpansion

:: ============================================
::  Podział dysku: C -> 45%  |  Z -> 55% (NTFS)
::  Wersja: 1.2 (bez etykiety C)
:: ============================================

:: --- Auto-elevacja do admina ---
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Brak uprawnien administratora. Ponawiam uruchomienie...
    powershell -NoProfile -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo.
echo [INFO] Odczytuje informacje o partycji C: ...

:: Pobranie numeru dysku i rozmiaru C: w MB (PowerShell)
for /f %%A in ('powershell -NoProfile -Command "(Get-Partition -DriveLetter C).DiskNumber"') do set "DiskNum=%%A"
for /f %%A in ('powershell -NoProfile -Command "[math]::Floor((Get-Volume -DriveLetter C).Size/1MB)"') do set "TotalMB=%%A"

if "%DiskNum%"=="" (
  echo [BLAD] Nie mozna ustalic numeru dysku dla C:. Przerywam.
  pause
  exit /b 1
)
if "%TotalMB%"=="" (
  echo [BLAD] Nie mozna ustalic rozmiaru partycji C:. Przerywam.
  pause
  exit /b 1
)

:: Wyliczenia – 55% shrink (czyli C: pozostaje 45%)
set /a ShrinkMB=TotalMB*55/100
set /a TargetCMB=TotalMB-ShrinkMB

echo [INFO] Rozmiar C: przed: %TotalMB% MB
echo [INFO] Planowany SHRINK: %ShrinkMB% MB  (docelowo C: ~%TargetCMB% MB, czyli ~45%% pierwotnej)
echo.

choice /M "Czy kontynuowac operacje partycjonowania"
if errorlevel 2 (
  echo [INFO] Uzytkownik anulowal operacje.
  pause
  exit /b 0
)

:: Tworzymy plik polecen dla diskpart
set "DPFILE=%TEMP%\_dp_shrink_createZ.txt"
del /f /q "%DPFILE%" >nul 2>&1

(
  echo rem === Wybor woluminu C i proba zmniejszenia o %ShrinkMB% MB ===
  echo select volume C
  echo shrink desired=%ShrinkMB%
  echo rem === Utworzenie nowej partycji z pozostalej przestrzeni ===
  echo select disk %DiskNum%
  echo create partition primary
  echo format fs=ntfs label^="Dane" quick
  echo assign letter^=Z
  echo detail partition
)>"%DPFILE%"

echo [INFO] Uruchamiam diskpart...
diskpart /s "%DPFILE%"
set "DPERR=%ERRORLEVEL%"

if not "%DPERR%"=="0" (
  echo.
  echo [BLAD] DiskPart zglosil blad (kod %DPERR%).
  echo       Typowe przyczyny: brak „skurczalnej” przestrzeni, hibernacja/pagefile,
  echo       ochrona systemu, BitLocker, albo litera F: zajeta.
  echo       Nic nie zostalo wymuszone. Sprawdz komunikaty diskpart powyzej.
  pause
  exit /b %DPERR%
)

:: Kontrola przypisania litery F
wmic logicaldisk get Name 2>nul | find /I "Z:" >nul
if errorlevel 1 (
  echo [UWAGA] Nie widac litery Z:. Byc moze byla zajeta przez naped optyczny/ISO.
) else (
  echo [OK] Utworzono partycje Z: (NTFS) z etykieta "Dane".
)

echo.
echo [ZAKONCZONE] C: ustawiono na ~45%% pierwotnej pojemnosci.
echo             Z: utworzono z reszty (~55%%) jako NTFS z etykieta "Dane".
echo.
pause
endlocal
