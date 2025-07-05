@echo off
echo ========================================
echo pMARS Windows Build Script
echo ========================================
echo.

cd src

echo Checking for GCC compiler...
gcc --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: GCC compiler not found!
    echo Please install MinGW-w64 or another GCC distribution.
    echo Add GCC to your system PATH and try again.
    pause
    exit /b 1
)

echo GCC found. Building pMARS...
echo.

echo Building basic version no graphics...
gcc -O -DEXT94 -DPERMUTATE -DRWLIMIT -o pmars_basic.exe pmars.c asm.c eval.c disasm.c cdb.c sim.c pos.c clparse.c global.c token.c str_eng.c

if %ERRORLEVEL% EQU 0 (
    echo Basic version built successfully: pmars_basic.exe
) else (
    echo Basic build failed!
    pause
    exit /b 1
)

echo.
echo Building version with text graphics...
gcc -O -DEXT94 -DPERMUTATE -DRWLIMIT -DGRAPHX -DDOSTXTGRAPHX -o pmars.exe pmars.c asm.c eval.c disasm.c cdb.c sim.c pos.c clparse.c global.c token.c str_eng.c

if %ERRORLEVEL% EQU 0 (
    echo Graphics version built successfully: pmars.exe
    set GRAPHICS_BUILD=1
) else (
    echo Graphics build failed, but basic version is available
    echo Copying basic version as main executable...
    copy pmars_basic.exe pmars.exe >nul
    set GRAPHICS_BUILD=0
)

echo.
echo ========================================
echo Build Summary
echo ========================================
if %GRAPHICS_BUILD% EQU 1 (
    echo pmars.exe with text graphics
) else (
    echo pmars.exe basic version, no graphics
)
echo pmars_basic.exe basic version backup
echo.

echo Testing with sample warriors...
echo.
pmars.exe ..\warriors\aeka.red ..\warriors\flashpaper.red

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Usage examples:
echo   pmars.exe warrior1.red warrior2.red
echo   pmars.exe -r 10 ..\warriors\aeka.red ..\warriors\flashpaper.red
echo   pmars.exe -e ..\warriors\aeka.red ..\warriors\flashpaper.red
echo.
echo For more information, see WINDOWS_BUILD_GUIDE.md
echo.
pause
