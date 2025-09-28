@echo off
setlocal EnableExtensions EnableDelayedExpansion
title TestVarment Mod4 Speedtest
chcp 65001 >nul

echo === TestVarment Mod4 Speedtest ===
echo.
set "FILENAME="
set /p FILENAME=Podaj nazwę pliku wynikowego (bez rozszerzenia) ^> 
if "%FILENAME%"=="" set "FILENAME=speedtest"

set "DESKTOP=%USERPROFILE%\Desktop"
set "OUTFILE=%DESKTOP%\%FILENAME%_speedtest.txt"

echo.
echo [1/4] Wykrywam typ połączenia...
set "CONNECTION=Nieznane"
REM Jeśli jest interfejs Wi-Fi i jest połączony – uznaj za Wi-Fi
netsh wlan show interfaces > "%TEMP%\_wlan.txt" 2>&1
findstr /i "SSID BSSID" "%TEMP%\_wlan.txt" >nul && (set "CONNECTION=Wi-Fi") || (set "CONNECTION=LAN")
del "%TEMP%\_wlan.txt" >nul 2>&1

echo.
echo [2/4] Szukam speedtest.exe...
set "SPEEDTEST="
if exist "%~dp0speedtest.exe" set "SPEEDTEST=%~dp0speedtest.exe"
if not defined SPEEDTEST (
  for /f "delims=" %%P in ('where speedtest 2^>nul') do set "SPEEDTEST=%%P"
)
if not defined SPEEDTEST (
  echo [BŁĄD] Nie znaleziono speedtest.exe.
  echo        Pobierz z https://www.speedtest.net/apps/cli i umiesc speedtest.exe obok tego skryptu
  echo        lub dodaj do PATH. Koncze.
  echo.
  pause
  exit /b 1
)

echo.
echo [3/4] Uruchamiam speedtest (to potrwa kilkadziesiąt sekund)...
set "TMPJSON=%TEMP%\speedtest_%RANDOM%.json"
"%SPEEDTEST%" -f json --accept-license --accept-gdpr > "%TMPJSON%" 2> "%TEMP%\speedtest_err.log"

if not exist "%TMPJSON%" (
  echo [BŁĄD] Plik z wynikiem nie powstał. Szczegóły: "%TEMP%\speedtest_err.log"
  echo.
  pause
  exit /b 2
)

echo.
echo [4/4] Zapisuje dane do pliku...
(
  echo === Wynik SpeedTest ===
  echo Data: %date% %time%
  echo Rodzaj: %CONNECTION%
) > "%OUTFILE%"

REM Parsowanie JSON i dopisanie do pliku (PowerShell)
powershell -NoProfile -Command ^
  "$j = Get-Content '%TMPJSON%' -Raw | ConvertFrom-Json;" ^
  "$isp = $j.isp;" ^
  "$srv = $j.server.name; $sid = $j.server.id;" ^
  "$ping = [math]::Round($j.ping.latency,2);" ^
  "$dl_mbps = [math]::Round(($j.download.bandwidth*8)/1e6,2);" ^
  "$ul_mbps = [math]::Round(($j.upload.bandwidth*8)/1e6,2);" ^
  "$dl_MBs  = [math]::Round($dl_mbps/8,2);" ^
  "$ul_MBs  = [math]::Round($ul_mbps/8,2);" ^
  "Add-Content -Path '%OUTFILE%' -Value @(" ^
  "'Serwer: ' + $srv + ' (ID ' + $sid + ')'," ^
  "'ISP: ' + $isp," ^
  "'Ping: ' + $ping + ' ms'," ^
  "'Pobieranie: ' + $dl_mbps + ' Mb/s  (' + $dl_MBs + ' MB/s)'," ^
  "'Wysyłanie: ' + $ul_mbps + ' Mb/s  (' + $ul_MBs + ' MB/s)'" ^
  ");"

del "%TMPJSON%" >nul 2>&1

echo  -> Wyniki zapisano do "%OUTFILE%"
echo.
endlocal
