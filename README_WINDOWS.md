# pMARS for Windows - Complete Setup Guide

This document provides everything you need to build and run pMARS (Portable Memory Array Redcode Simulator) on Windows systems.

## What is pMARS?

pMARS is a Core War simulator that allows you to run battles between Redcode programs (called "warriors"). Core War is a programming game where players write programs that attempt to destroy each other in a shared memory space.

## Quick Setup (3 Steps)

### 1. Install GCC Compiler
Download and install **MinGW-w64** from: https://www.mingw-w64.org/downloads/
- Choose the installer for your system (32-bit or 64-bit)
- Add the `bin` directory to your Windows PATH
- Verify installation: Open Command Prompt and run `gcc --version`

### 2. Build pMARS
- Double-click `build.bat` in the project root directory
- Or run from Command Prompt: `.\build.bat`
- The script will automatically build both basic and graphics versions

### 3. Run Your First Battle
```cmd
cd src
pmars.exe ..\warriors\aeka.red ..\warriors\flashpaper.red
```

## What You Get

After building, you'll have:
- **`pmars.exe`** - Main executable (with graphics if supported)
- **`pmars_basic.exe`** - Backup version without graphics
- **Sample warriors** in the `warriors/` directory
- **Complete documentation** in the `doc/` directory

## Documentation Files

| File | Purpose |
|------|---------|
| `WINDOWS_BUILD_GUIDE.md` | Complete build and usage guide |
| `QUICK_REFERENCE.md` | Essential commands and options |
| `build.bat` | Automated build script |
| `README_WINDOWS.md` | This overview document |

## Basic Usage Examples

```cmd
# Simple battle
pmars.exe warrior1.red warrior2.red

# Multiple rounds for statistics
pmars.exe -r 100 warrior1.red warrior2.red

# Enter debugger mode
pmars.exe -e warrior1.red warrior2.red

# Use different core size
pmars.exe -s 4000 warrior1.red warrior2.red

# Permutate starting positions
pmars.exe -P -r 100 warrior1.red warrior2.red
```

## Visualizer Information

**Current Status**: The Windows build includes basic text output and debugging capabilities. Full graphical visualization is not available due to Windows compatibility limitations with the original graphics libraries.

**Available Display Options**:
- Text-based output showing warrior code and results
- Step-by-step debugger mode (`-e` flag)
- Verbose assembly output (`-V` flag)

**For Advanced Graphics**: Consider using the Linux version under WSL (Windows Subsystem for Linux) or third-party Core War visualizers.

## Creating Your First Warrior

Create a file called `mywarrior.red`:
```redcode
;name My First Warrior
;author Your Name
;strategy Simple bomber

bomb    dat #0, #0
start   mov bomb, @2
        add #1, start
        jmp start
```

Run it against another warrior:
```cmd
pmars.exe mywarrior.red ..\warriors\aeka.red
```

## Troubleshooting

### Build Issues
- **"gcc: command not found"** → Install MinGW-w64 and add to PATH
- **Build script fails** → Run commands manually from `WINDOWS_BUILD_GUIDE.md`
- **Graphics build fails** → Use basic version, it works the same for battles

### Runtime Issues
- **"Warriors not found"** → Check file paths, use `..` for parent directory
- **Slow performance** → Use smaller core size (`-s 4000`) or basic version

## Performance Tips

1. **For Tournaments**: Use `pmars_basic.exe` for fastest execution
2. **Statistical Analysis**: Use `-r 1000` or higher for meaningful results
3. **Memory Usage**: Smaller core sizes (`-s 4000`) use less memory and run faster
4. **Multiple Warriors**: You can run up to 4 warriors in one battle

## Next Steps

1. **Read the Documentation**: Check `doc/redcode.ref` for Redcode language reference
2. **Study Examples**: Examine warriors in the `warriors/` directory
3. **Join the Community**: Search for "Core War" communities online
4. **Write Warriors**: Start with simple strategies and gradually increase complexity

## Support

- **Complete Build Guide**: See `WINDOWS_BUILD_GUIDE.md`
- **Quick Commands**: See `QUICK_REFERENCE.md`
- **Original Documentation**: Check the `doc/` directory
- **Core War FAQ**: See `doc/corewar-faq.html`

---

**Version**: pMARS v0.9.4 for Windows
**Tested On**: Windows 10/11 with MinGW-w64
**Last Updated**: 2025

Happy Core War programming! 🚀
