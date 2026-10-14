@echo off
echo ===============================
echo   Build Python ke EXE (PyInstaller)
echo ===============================
echo.

REM pastikan ada file download_swift_100%.py di folder ini
if not exist download_swift_100.py (
    echo File download_swift_100.py tidak ditemukan!
    pause
    exit
)

REM jalankan pyinstaller
pyinstaller --onefile --noconsole --icon=icon.ico download_swift_100.py

echo.
echo ===============================
echo   Build selesai!
echo   Cek folder "dist" untuk EXE.
echo ===============================
pause
