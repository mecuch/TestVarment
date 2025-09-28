@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

REM === KONFIGURACJA (dopasuj do głównego skryptu) ===
REM === AUTODETEKCJA LITERY PENDRIVE'A (na podstawie ścieżki tego .BAT) ===
set "USB_LETTER=%~d0"
set "USB_LETTER=%USB_LETTER::=%"

echo Wykryta litera pendrive: %USB_LETTER%:

set "DEST_LETTER=Z"
set "DEST_DIR_NAME=SRODOWISKO_TESTOWE"
set "REPO_DIR_NAME=repository"
set "URL_DIR_NAME=URL"

set "SHORTCUT_NAME1=BatteryInfoView"
set "SHORTCUT_NAME2=CristalDiskInfo"
set "SHORTCUT_NAME3=FurMark"
set "SHORTCUT_NAME4=HWiNFO64"
set "SHORTCUT_NAME5=IsMyLcdOK_x64"
set "SHORTCUT_NAME6=OCCT"
set "SHORTCUT_NAME7=HDTune"

set "DESKTOP=%USERPROFILE%\Desktop"

echo.
echo SPRZĄTANIE...

REM === 1) Usuń katalog repozytorium ===
set "REPO_PATH=%DEST_LETTER%:\%DEST_DIR_NAME%\%REPO_DIR_NAME%"
if exist "%REPO_PATH%\" (
    echo Usuwam katalog repo: "%REPO_PATH%"
    rmdir /S /Q "%REPO_PATH%"
) else (
    echo [INFO] Katalog repo nie istnieje: "%REPO_PATH%"
)

REM === 2) Usuń skróty .lnk utworzone przez główny skrypt ===
for %%I in (1 2 3 4 5 6 7) do (
    set "LNK=!DESKTOP!\!SHORTCUT_NAME%%I!.lnk"
    if exist "!LNK!" (
        del /Q "!LNK!"
        echo Usunięto: "!LNK!"
    ) else (
        echo [INFO] Brak: "!LNK!"
    )
)

echo Sprzątanie zakończone.
endlocal
