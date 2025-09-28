@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

REM === KONFIGURACJA ===
set "TARGET_EXE1=Z:\SRODOWISKO_TESTOWE\repository\BATTERYINFO\BatteryInfoView.exe"
set "SHORTCUT_NAME1=BatteryInfoView"

set "TARGET_EXE2=Z:\SRODOWISKO_TESTOWE\repository\CRISTALDISKINFO\DiskInfo64K.exe"
set "SHORTCUT_NAME2=CristalDiskInfo"

set "TARGET_EXE3=Z:\SRODOWISKO_TESTOWE\repository\FURMARK\FurMark.exe"
set "SHORTCUT_NAME3=FurMark"

set "TARGET_EXE4=Z:\SRODOWISKO_TESTOWE\repository\HWINFO\HWiNFO64.exe"
set "SHORTCUT_NAME4=HWiNFO64"

set "TARGET_EXE5=Z:\SRODOWISKO_TESTOWE\repository\ISMYLCDOK\IsMyLcdOK_x64.exe"
set "SHORTCUT_NAME5=IsMyLcdOK_x64"

set "TARGET_EXE6=Z:\SRODOWISKO_TESTOWE\repository\OCCT\OCCT.exe"
set "SHORTCUT_NAME6=OCCT"

set "TARGET_EXE7=Z:\SRODOWISKO_TESTOWE\repository\HDTUNE\HDTune.exe"
set "SHORTCUT_NAME7=HDTune"


REM === AUTODETEKCJA LITERY PENDRIVE'A (na podstawie ścieżki tego .BAT) ===
set "USB_LETTER=%~d0"
set "USB_LETTER=%USB_LETTER::=%"
echo Wykryta litera pendrive: %USB_LETTER%:

set "DEST_LETTER=Z"
set "DEST_DIR_NAME=SRODOWISKO_TESTOWE"
set "REPO_DIR_NAME=repository"
set "ROBO_FLAGS=/E /R:1 /W:1"

REM === TWORZENIE KATALOGU DOCELOWEGO ===
if not exist "%DEST_LETTER%:\%DEST_DIR_NAME%" mkdir "%DEST_LETTER%:\%DEST_DIR_NAME%"

REM === KOPIOWANIE REPOZYTORIUM ===
set "SRC_PATH=%USB_LETTER%:\%REPO_DIR_NAME%"
set "DST_PATH=%DEST_LETTER%:\%DEST_DIR_NAME%\%REPO_DIR_NAME%"

if not exist "%SRC_PATH%" (
  echo Nie znaleziono folderu "%SRC_PATH%".
  pause & exit /b 1
)

echo Kopiowanie z "%SRC_PATH%" do "%DST_PATH%"...
robocopy "%SRC_PATH%" "%DST_PATH%" %ROBO_FLAGS%
set RC=%ERRORLEVEL%

if %RC% GTR 7 (
  echo Robocopy zwrocilo kod %RC%. Przerwano tworzenie skrotow.
  pause & exit /b %RC%
)

REM === TWORZENIE SKRÓTÓW (z ustawionym WorkingDirectory) ===
echo Tworzenie skrotow na pulpicie...

powershell -NoProfile -Command ^
  "$ws=New-Object -ComObject WScript.Shell; $p='%TARGET_EXE1%'; $sc=$ws.CreateShortcut([Environment]::GetFolderPath('Desktop')+'\%SHORTCUT_NAME1%.lnk'); $sc.TargetPath=$p; $sc.WorkingDirectory=(Split-Path $p -Parent); $sc.IconLocation=$p+',0'; $sc.WindowStyle=1; $sc.Save()"
echo Stworzono skrot \%SHORTCUT_NAME1%.lnk

powershell -NoProfile -Command ^
  "$ws=New-Object -ComObject WScript.Shell; $p='%TARGET_EXE2%'; $sc=$ws.CreateShortcut([Environment]::GetFolderPath('Desktop')+'\%SHORTCUT_NAME2%.lnk'); $sc.TargetPath=$p; $sc.WorkingDirectory=(Split-Path $p -Parent); $sc.IconLocation=$p+',0'; $sc.WindowStyle=1; $sc.Save()"
echo Stworzono skrot \%SHORTCUT_NAME2%.lnk

powershell -NoProfile -Command ^
  "$ws=New-Object -ComObject WScript.Shell; $p='%TARGET_EXE3%'; $sc=$ws.CreateShortcut([Environment]::GetFolderPath('Desktop')+'\%SHORTCUT_NAME3%.lnk'); $sc.TargetPath=$p; $sc.WorkingDirectory=(Split-Path $p -Parent); $sc.IconLocation=$p+',0'; $sc.WindowStyle=1; $sc.Save()"
echo Stworzono skrot \%SHORTCUT_NAME3%.lnk

powershell -NoProfile -Command ^
  "$ws=New-Object -ComObject WScript.Shell; $p='%TARGET_EXE4%'; $sc=$ws.CreateShortcut([Environment]::GetFolderPath('Desktop')+'\%SHORTCUT_NAME4%.lnk'); $sc.TargetPath=$p; $sc.WorkingDirectory=(Split-Path $p -Parent); $sc.IconLocation=$p+',0'; $sc.WindowStyle=1; $sc.Save()"
echo Stworzono skrot \%SHORTCUT_NAME4%.lnk

powershell -NoProfile -Command ^
  "$ws=New-Object -ComObject WScript.Shell; $p='%TARGET_EXE5%'; $sc=$ws.CreateShortcut([Environment]::GetFolderPath('Desktop')+'\%SHORTCUT_NAME5%.lnk'); $sc.TargetPath=$p; $sc.WorkingDirectory=(Split-Path $p -Parent); $sc.IconLocation=$p+',0'; $sc.WindowStyle=1; $sc.Save()"
echo Stworzono skrot \%SHORTCUT_NAME5%.lnk

powershell -NoProfile -Command ^
  "$ws=New-Object -ComObject WScript.Shell; $p='%TARGET_EXE6%'; $sc=$ws.CreateShortcut([Environment]::GetFolderPath('Desktop')+'\%SHORTCUT_NAME6%.lnk'); $sc.TargetPath=$p; $sc.WorkingDirectory=(Split-Path $p -Parent); $sc.IconLocation=$p+',0'; $sc.WindowStyle=1; $sc.Save()"
echo Stworzono skrot \%SHORTCUT_NAME6%.lnk

powershell -NoProfile -Command ^
  "$ws=New-Object -ComObject WScript.Shell; $p='%TARGET_EXE7%'; $sc=$ws.CreateShortcut([Environment]::GetFolderPath('Desktop')+'\%SHORTCUT_NAME7%.lnk'); $sc.TargetPath=$p; $sc.WorkingDirectory=(Split-Path $p -Parent); $sc.IconLocation=$p+',0'; $sc.WindowStyle=1; $sc.Save()"
echo Stworzono skrot \%SHORTCUT_NAME7%.lnk

if %ERRORLEVEL% NEQ 0 (
    echo Blad przy tworzeniu skrotow.
    pause
    exit /b 1
)
echo Wszystkie skroty utworzone na pulpicie!

endlocal
