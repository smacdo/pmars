# pMARS Windows Quick Reference

## Quick Start
1. **Build**: Double-click `build.bat` or run it from command line
2. **Run**: `cd src` then `pmars.exe warrior1.red warrior2.red`

## Essential Commands

### Building
```cmd
# Navigate to project root and run:
build.bat

# Or manually in src directory:
gcc -O -DEXT94 -DPERMUTATE -DRWLIMIT -o pmars.exe pmars.c asm.c eval.c disasm.c cdb.c sim.c pos.c clparse.c global.c token.c str_eng.c
```

### Running Battles
```cmd
# Basic battle
pmars.exe warrior1.red warrior2.red

# With provided warriors
pmars.exe ..\warriors\aeka.red ..\warriors\flashpaper.red

# Multiple rounds for statistics
pmars.exe -r 100 warrior1.red warrior2.red

# Enter debugger mode
pmars.exe -e warrior1.red warrior2.red
```

### Common Options
| Option | Description | Example |
|--------|-------------|---------|
| `-r #` | Number of rounds | `-r 100` |
| `-s #` | Core size | `-s 4000` |
| `-c #` | Cycles until tie | `-c 40000` |
| `-e` | Enter debugger | `-e` |
| `-P` | Permutate positions | `-P` |
| `-V` | Verbose assembly | `-V` |
| `-b` | Brief mode | `-b` |

### File Locations
- **Executable**: `src/pmars.exe`
- **Warriors**: `warriors/*.red`
- **Documentation**: `doc/`
- **Build Guide**: `WINDOWS_BUILD_GUIDE.md`

### Troubleshooting
- **Build fails**: Check if GCC is installed and in PATH
- **Graphics issues**: Use basic build without `-DGRAPHX`
- **Missing warriors**: Check file paths and use `..` for parent directory

### Example Warrior (save as `test.red`)
```redcode
;name Test Warrior
;author Your Name

start   mov #1, 2
        jmp start
```

### Performance Tips
- Use `-r 1000` for statistical significance
- Smaller core (`-s 4000`) runs faster
- Use `pmars_basic.exe` for fastest execution
- Multiple warriors: `pmars.exe w1.red w2.red w3.red w4.red`

For complete documentation, see `WINDOWS_BUILD_GUIDE.md`
