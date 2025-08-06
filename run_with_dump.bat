@echo off
echo Running pMARS with memory dump enabled...
echo.

REM Set the dump file name
set PMARS_DUMP_FILE=battle_dump.json

REM Check if warriors exist
if not exist "warriors\aeka.red" (
    echo Error: Warrior files not found in warriors directory
    pause
    exit /b 1
)

REM Run the battle with a short cycle limit for demo
echo Running battle: Aeka vs Flashpaper
echo Dump file: %PMARS_DUMP_FILE%
echo.

cd src
pmars.exe -c 1000 ..\warriors\aeka.red ..\warriors\flashpaper.red

echo.
echo Battle completed!
if exist "..\%PMARS_DUMP_FILE%" (
    echo Memory dump saved to: %PMARS_DUMP_FILE%
    echo File size:
    dir "..\%PMARS_DUMP_FILE%" | find "%PMARS_DUMP_FILE%"
) else (
    echo Warning: No dump file was created. Memory dumping may not be integrated yet.
)

echo.
echo To visualize the battle, run:
echo python visualizer_example.py %PMARS_DUMP_FILE%
echo.
pause
