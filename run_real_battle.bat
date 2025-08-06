@echo off
echo ========================================
echo Running Real pMARS Battle with Memory Dump
echo ========================================
echo.

REM Set environment variable for memory dump
set PMARS_DUMP_FILE=real_battle.json

echo Setting up battle: Aeka vs Flashpaper
echo Dump file: %PMARS_DUMP_FILE%
echo Limiting cycles to 2000 for manageable dump size
echo.

REM Use existing pMARS executable with memory dump support
echo Using existing pMARS executable with memory dump support...
cd src

if not exist "pmars_dump.exe" (
    echo pmars_dump.exe not found! Please run build.bat first.
    cd ..
    pause
    exit /b 1
)

echo.
echo Running battle with limited cycles...
pmars_dump.exe -c 2000 ..\warriors\rave.red ..\warriors\flashpaper.red

echo.
echo Battle completed!
cd ..

if exist "real_battle.json" (
    echo Real battle dump file found: real_battle.json
    echo File size:
    dir "real_battle.json" | find "real_battle.json"
    echo.
    echo Starting pygame visualizer with real battle data...
    python visualizer_example.py real_battle.json
) else (
    echo Real battle dump file not found. Using sample data instead...
    echo Starting pygame visualizer with sample data...
    python visualizer_example.py sample_battle.json
)

pause
