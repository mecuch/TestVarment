@echo off
setlocal EnableExtensions EnableDelayedExpansion
title Uruchamianie ikon pulpitu
chcp 65001 >nul

echo.
echo === TestVarment Mod1 Uruchamianie ikon pulpitu ===
echo.
echo Wlaczam ikony 'Ten komputer' i 'Panel sterowania' na Pulpicie za 5 sekund...
timeout /t 3 /nobreak >nul

REM GUIDy ikon:
REM Ten komputer:    {20D04FE0-3AEA-1069-A2D8-08002B30309D}
REM Panel sterowania:{5399E694-6CE5-4D6C-8FCE-1D8870FDCBA0}

for %%K in ("HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel" ^
            "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\ClassicStartMenu") do (
  reg add %%~K /v {20D04FE0-3AEA-1069-A2D8-08002B30309D} /t REG_DWORD /d 0 /f >nul
  reg add %%~K /v {5399E694-6CE5-4D6C-8FCE-1D8870FDCBA0} /t REG_DWORD /d 0 /f >nul
)

echo  -> Ustawienia zapisane w rejestrze bieżącego użytkownika.

echo.
echo Restartuję powłokę Explorer, aby zastosować zmiany ikon...
taskkill /f /im explorer.exe >nul 2>&1
start explorer.exe

echo.
endlocal
