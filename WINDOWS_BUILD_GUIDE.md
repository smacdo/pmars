# pMARS Windows Build and Run Guide

This guide provides step-by-step instructions for building and running pMARS (Portable Memory Array Redcode Simulator) on Windows systems.

## Prerequisites

### Required Software
1. **GCC Compiler** - You need a GCC compiler installed on your Windows system. Options include:
   - **MinGW-w64** (Recommended)
   - **MSYS2** with GCC
   - **TDM-GCC**
   - **Windows Subsystem for Linux (WSL)** with GCC

### Verify GCC Installation
Open Command Prompt or PowerShell and run:
```cmd
gcc --version
```
You should see output similar to:
```
gcc (MinGW-w64 x86_64-posix-seh-rev0, Built by MinGW-w64 project) 8.1.0
```

## Building pMARS

### Step 1: Navigate to Source Directory
```cmd
cd "c:\path\to\your\pmars\src"
```

### Step 2: Build Options

#### Option A: Basic Build (No Graphics)
For a simple command-line version without visual display:
```cmd
gcc -O -DEXT94 -DPERMUTATE -DRWLIMIT -o pmars.exe pmars.c asm.c eval.c disasm.c cdb.c sim.c pos.c clparse.c global.c token.c str_eng.c
```

#### Option B: Build with Text Graphics (Recommended)
For a version with basic text-based visualization:
```cmd
gcc -O -DEXT94 -DPERMUTATE -DRWLIMIT -DGRAPHX -DDOSTXTGRAPHX -o pmars.exe pmars.c asm.c eval.c disasm.c cdb.c sim.c pos.c clparse.c global.c token.c str_eng.c
```

**Note:** The graphics version may have compatibility issues on some Windows systems. If it fails to build, use Option A.

### Step 3: Verify Build
After successful compilation, you should see `pmars.exe` in the `src` directory. Test it:
```cmd
.\pmars.exe
```

## Compiler Flags Explained

- `-O` - Enable optimization
- `-DEXT94` - Enable ICWS'94 extensions (SEQ, SNE, NOP opcodes and new addressing modes)
- `-DPERMUTATE` - Enable position permutation support (-P switch)
- `-DRWLIMIT` - Enable read/write limits (-R and -W switches)
- `-DGRAPHX` - Enable graphics display support
- `-DDOSTXTGRAPHX` - Enable DOS-style text graphics (Windows compatible)

## Running pMARS

### Basic Usage
```cmd
.\pmars.exe warrior1.red warrior2.red
```

### Example with Provided Warriors
```cmd
.\pmars.exe ..\warriors\aeka.red ..\warriors\flashpaper.red
```

### Common Command Line Options

#### Basic Options
- `-r #` - Number of rounds to play (default: 1)
- `-s #` - Size of core memory (default: 8000)
- `-c #` - Cycles until tie (default: 80000)
- `-p #` - Maximum processes per warrior (default: 8000)
- `-l #` - Maximum warrior length (default: 100)

#### Advanced Options
- `-d #` - Minimum distance between warriors
- `-F #` - Fixed position for warrior #2
- `-P` - Permutate starting positions
- `-e` - Enter debugger mode
- `-b` - Brief mode (no source listings)
- `-V` - Verbose assembly output
- `-k` - Output in King of the Hill format

#### Examples
```cmd
# Run 100 rounds
.\pmars.exe -r 100 warrior1.red warrior2.red

# Use smaller core size
.\pmars.exe -s 4000 warrior1.red warrior2.red

# Enable debugger
.\pmars.exe -e warrior1.red warrior2.red

# Multiple options
.\pmars.exe -r 10 -s 4000 -P warrior1.red warrior2.red
```

## Visualizer and Graphics

### Current Status
The current Windows build supports basic text output but does not include a full graphical visualizer due to Windows compatibility limitations with the original graphics libraries.

### Available Display Options
1. **Text Output** - Shows warrior code and battle results
2. **Debugger Mode** - Use `-e` flag to step through execution
3. **Verbose Mode** - Use `-V` flag for detailed assembly output

### For Advanced Graphics
If you need advanced graphics visualization, consider:
1. Using the Linux version under WSL
2. Using a third-party Core War visualizer
3. Building with additional graphics libraries (requires advanced setup)

## Troubleshooting

### Build Issues

#### "gcc: command not found"
- Install MinGW-w64 or another GCC distribution
- Add GCC to your system PATH
- Restart Command Prompt/PowerShell after installation

#### "fatal error: curses.h: No such file or directory"
- This occurs when trying to build with curses graphics
- Use the basic build option (Option A) instead
- Or install PDCurses library for Windows

#### Compilation errors with graphics
- Use the non-graphics build option
- Ensure you're using the correct compiler flags

### Runtime Issues

#### "The program can't start because of missing DLL"
- Install Microsoft Visual C++ Redistributable
- Or use static linking: add `-static` flag to gcc command

#### Warriors not found
- Check file paths are correct
- Use relative paths: `..\warriors\filename.red`
- Ensure warrior files exist in the warriors directory

## File Structure

After successful build, your directory should contain:
```
pmars/
├── src/
│   ├── pmars.exe          # Main executable
│   ├── pmars_nogfx.exe    # Non-graphics version (if built)
│   └── [source files]
├── warriors/
│   ├── aeka.red
│   ├── flashpaper.red
│   └── [other warriors]
└── config/
    └── [configuration files]
```

## Creating Your Own Warriors

Warriors are written in Redcode assembly language. Example:
```redcode
;name My First Warrior
;author Your Name

start   mov #1, 2
        jmp start
```

Save as `.red` file and run with pMARS.

## Additional Resources

- **Original README**: See `README` file for original documentation
- **Redcode Reference**: Check `doc/redcode.ref` for language reference
- **Core War FAQ**: See `doc/corewar-faq.html`
- **Configuration Files**: Use files in `config/` directory for different rule sets

## Performance Tips

1. Use `-O2` or `-O3` for better optimization (may increase build time)
2. For tournaments, use the non-graphics version for faster execution
3. Adjust core size (`-s`) based on your needs - smaller cores run faster
4. Use multiple rounds (`-r`) for statistical significance

## Example Build Script

Create a batch file `build.bat`:
```batch
@echo off
cd src
echo Building pMARS for Windows...
gcc -O -DEXT94 -DPERMUTATE -DRWLIMIT -o pmars.exe pmars.c asm.c eval.c disasm.c cdb.c sim.c pos.c clparse.c global.c token.c str_eng.c
if %ERRORLEVEL% EQU 0 (
    echo Build successful! pmars.exe created.
    echo Testing with sample warriors...
    pmars.exe ..\warriors\aeka.red ..\warriors\flashpaper.red
) else (
    echo Build failed. Check for errors above.
)
pause
```

Run with: `build.bat`

---

**Note**: This guide is based on pMARS v0.9.4 and has been tested on Windows 10/11 with MinGW-w64. Your experience may vary depending on your specific Windows version and compiler setup.
