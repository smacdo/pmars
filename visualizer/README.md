# CoreWar Battle Visualizer

A professional-grade pygame-based visualizer for replaying recorded CoreWar battles from `.viz` files. This system provides complete visual representation of CoreWar battles with interactive controls, real-time memory visualization, and video recording capabilities.

## 🎉 Latest Updates

- **✅ 64-Character Warrior Names**: Full support for long, descriptive warrior names (up to 64 characters)
- **✅ Enhanced Binary Format**: 160-byte header with improved data structure
- **✅ Professional Visualization**: Complete memory grid, execution trails, and activity indicators
- **✅ Full Integration**: Seamless recording and playback workflow with pmars
- **🎬 Video Recording**: Export battles as MP4 videos with customizable settings
- **⚡ Auto-Speed Mode**: Automatic speed calculation for target durations
- **🎯 Victory Animations**: Animated victory screens with particle effects
- **📊 Battle Statistics**: Real-time warrior elimination tracking
- **🖥️ Headless Mode**: Server-friendly video generation without display requirements

## Requirements

- **Python 3.6+**
- **pygame library**
- **opencv-python** (for video recording)
- **numpy** (for video recording)

## Installation

Install required dependencies:

```bash
pip install pygame
pip install opencv-python  # For video recording
pip install numpy          # For video recording
```

## Usage

### Recording Battles

Use the enhanced pmars simulator with the `-T` option to record battles:

```bash
# Record a battle to visualization file
pmars_full_viz.exe -T my_battle.viz warrior1.red warrior2.red

# Example with long warrior names and energy enabled
pmars_full_viz.exe -E -T epic_battle.viz "Advanced_Combat_Unit.red" "Tactical_Strike_Force.red"
```

### Interactive Visualization

Run the visualizer with any `.viz` file:

```bash
python visualizer.py <battle.viz>
```

**Examples:**
```bash
# Basic interactive mode
python visualizer.py ../test_battle.viz

# Auto-speed mode for long battles (30-second duration)
python visualizer.py ../large_battle.viz --interactive-duration 30

# Display help
python visualizer.py --help
```

### Video Recording

Generate MP4 videos of battles:

```bash
# Basic video recording (auto-generated filename)
python visualizer.py battle.viz --record

# Custom video settings
python visualizer.py battle.viz --record --output my_battle.mp4 --fps 60

# 10-second video with auto-calculated speed
python visualizer.py battle.viz --record --duration 10

# High-quality video for presentation
python visualizer.py battle.viz --record --duration 15 --fps 60 --output presentation.mp4
```

## 🎮 Interactive Controls

| Key | Action |
|-----|--------|
| **SPACE** | Play/Pause animation |
| **RIGHT ARROW** | Step one event forward |
| **LEFT ARROW** | Step one event backward |
| **UP ARROW** | Speed up animation (2x) |
| **DOWN ARROW** | Slow down animation (0.5x) |
| **HOME** | Restart from beginning |
| **END** | Jump to end of battle |
| **ESC** | Exit visualizer |

## 🎨 Visual Elements

### Memory Grid Display
- **Each cell** represents one memory location in the core
- **Grid layout** automatically calculated for optimal viewing (80x100 for 8000 core)
- **Real-time updates** showing warrior control and activity

### Color Coding
| Color | Meaning |
|-------|---------|
| **Red** | Warrior 1 controlled memory |
| **Blue** | Warrior 2 controlled memory |
| **Yellow** | Execution trail (fading) |
| **Green** | Memory reads (flashing) |
| **Orange** | Memory writes/modifications (flashing) |
| **Gray** | Empty/neutral memory |

### Information Panel
- **Battle Statistics**: Core size, total cycles, event count
- **Warrior Information**: Names (up to 64 chars), starting positions, elimination status
- **Progress Tracking**: Current cycle, event position, progress bar
- **Real-time Status**: Playing/paused, current animation speed
- **Controls Reference**: Key bindings and usage instructions

### Victory Screen
- **Animated Results**: Pulsing victory text with particle effects
- **Battle Summary**: Final statistics and elimination details
- **Visual Effects**: Glowing text, floating particles, smooth animations

## 🎬 Video Recording Features

### Supported Formats
- **MP4**: High-quality video output using OpenCV
- **Customizable FPS**: 30, 60, or any frame rate
- **Headless Mode**: Generate videos without display requirements

### Duration Control
- **Target Duration**: Automatically calculate speed for desired video length
- **Manual Speed**: Override with specific events per second
- **Victory Screen**: Includes 3-second animated victory sequence

### Quality Settings
```bash
# Different quality presets
python visualizer.py battle.viz --record --fps 30 --duration 10    # Standard
python visualizer.py battle.viz --record --fps 60 --duration 15    # High quality
python visualizer.py battle.viz --record --fps 30 --speed 500      # Manual speed
```

## ⚙️ Configuration

Customize the visualization by editing the configuration section at the top of `visualizer.py`:

### Animation Settings
```python
ANIMATION_SPEED = 15.0      # Events per second during playback
WINDOW_WIDTH = 1400         # Window width in pixels
WINDOW_HEIGHT = 900         # Window height in pixels
```

### Memory Visualization
```python
MAX_CELL_SIZE = 10          # Maximum size per memory cell
MIN_CELL_SIZE = 2           # Minimum size per memory cell
EXECUTION_TRAIL_LENGTH = 30 # Number of recent executions to show
EXECUTION_FADE_SPEED = 0.8  # How fast effects fade (0.0-1.0)
```

### Visual Appearance
```python
COLOR_BACKGROUND = (20, 20, 30)      # Dark blue background
COLOR_WARRIOR1 = (255, 80, 80)       # Warrior 1 (red)
COLOR_WARRIOR2 = (80, 120, 255)      # Warrior 2 (blue)
COLOR_EXECUTION = (255, 255, 100)    # Execution trail (yellow)
# ... and many more customizable colors
```

## 📊 .viz File Format

The visualizer reads binary `.viz` files with the following specifications:

### Header Structure (160 bytes)
- **Magic Number**: "PMARSREC" (8 bytes)
- **Version**: Format version (4 bytes)
- **Core Settings**: Size, cycles, event count (12 bytes)
- **Warrior 1 Name**: Up to 64 characters (64 bytes)
- **Warrior 2 Name**: Up to 64 characters (64 bytes)
- **Starting Positions**: Warrior placement (8 bytes)
- **Reserved**: Future expansion (8 bytes)

### Event Records (12 bytes each)
- **Cycle Number**: Current simulation cycle
- **Memory Address**: Location of activity
- **Warrior ID**: Which warrior (0 or 1)
- **Event Type**: Execution, read, write, elimination, etc.
- **Context Data**: Additional event-specific information

## 🚀 Features

### Core Functionality
- ✅ **Real-time or step-by-step battle replay**
- ✅ **Visual memory ownership tracking**
- ✅ **Animated execution trails with fading**
- ✅ **Memory access activity indicators**
- ✅ **Complete battle progress tracking**
- ✅ **Configurable animation speed and appearance**

### Advanced Features
- ✅ **64-character warrior name support**
- ✅ **Professional UI with statistics panel**
- ✅ **Interactive playback controls with speed adjustment**
- ✅ **Automatic memory layout optimization**
- ✅ **Color-coded memory activity**
- ✅ **Progress bar and status indicators**
- ✅ **Warrior elimination tracking**
- ✅ **Animated victory screens with effects**

### Video Recording Features
- ✅ **MP4 video export with OpenCV**
- ✅ **Headless mode for server deployment**
- ✅ **Auto-speed calculation for target durations**
- ✅ **Customizable frame rates and quality**
- ✅ **Automatic filename generation**
- ✅ **Victory screen recording**

### Technical Features
- ✅ **Efficient binary file format**
- ✅ **Cross-platform pygame compatibility**
- ✅ **Configurable display settings**
- ✅ **Robust error handling**
- ✅ **Memory-efficient visualization**
- ✅ **High-speed processing for large battles**

## 📝 Example Workflows

### Basic Battle Visualization
```bash
# 1. Create simple warriors
echo ';name Bomber' > bomber.red
echo 'DAT #0, #0' >> bomber.red

# 2. Record battle
pmars_full_viz.exe -T basic_battle.viz bomber.red ../warriors/aeka.red

# 3. Visualize
python visualizer.py basic_battle.viz
```

### Advanced Battle with Long Names
```bash
# 1. Record battle with descriptive names and energy enabled
pmars_full_viz.exe -e -T advanced_battle.viz \
  "Advanced_Reconnaissance_Unit_Alpha_Seven_Deployment_System.red" \
  "Tactical_Strike_Force_Beta_Nine_Advanced_Combat_System_Protocol.red"

# 2. View with auto-speed for 30-second duration
python visualizer.py advanced_battle.viz --interactive-duration 30
```

### Video Generation for Presentation
```bash
# 1. Record complex battle
pmars_full_viz.exe -e -T presentation_battle.viz warrior1.red warrior2.red

# 2. Generate high-quality video
python visualizer.py presentation_battle.viz \
  --record --duration 15 --fps 60 --output presentation.mp4

# 3. The video will include:
#    - Complete battle visualization
#    - Animated victory screen
#    - Automatically calculated optimal speed
```

### Server-side Video Generation
```bash
# Headless mode for server deployment (no display required)
python visualizer.py battle.viz --record --duration 10 --output server_video.mp4

# Batch processing multiple battles
for viz in *.viz; do
    python visualizer.py "$viz" --record --duration 12 --output "${viz%.viz}.mp4"
done
```

## 🔧 Development Tools

### Test Script
Use `test_viz.py` to inspect `.viz` file contents:

```bash
python test_viz.py battle.viz
```

**Example Output:**
```
Testing battle.viz...
Header size: 160 bytes
Magic: 'PMARSREC'
Version: 1
Core size: 8000
Total cycles: 80000
Total events: 1247
Warrior 1: 'Advanced Reconnaissance Unit Alpha-Seven Deployment System' at 1500
Warrior 2: 'Tactical Strike Force Beta-Nine Advanced Combat System Protocol' at 3500
Event 0: cycle=1, addr=1500, warrior=0, type=0, data=160000
...
```

## 🎯 Performance Tips

1. **Large Battles**: Use `--interactive-duration` for auto-speed calculation
2. **Video Recording**: Higher FPS produces smoother but larger videos
3. **Memory Usage**: Smaller core sizes render faster
4. **Visual Quality**: Adjust `MAX_CELL_SIZE` for different screen sizes
5. **Headless Mode**: Use for server-side video generation

## 🐛 Troubleshooting

### Common Issues
- **"Invalid viz file"**: Check that file was created with `-T` option
- **Graphics issues**: Update pygame: `pip install --upgrade pygame`
- **Video recording fails**: Install OpenCV: `pip install opencv-python`
- **Slow performance**: Use `--interactive-duration` for large battles
- **Missing events**: Ensure pmars_full_viz.exe is used for recording

### Video Recording Issues
- **"OpenCV not available"**: Install with `pip install opencv-python`
- **Codec errors**: Try different output filenames or update OpenCV
- **Headless mode fails**: Set SDL_VIDEODRIVER=dummy environment variable

### Debugging
- Use `test_viz.py` to verify file format
- Check warrior names don't exceed 64 characters
- Verify dependencies: `python -c "import pygame, cv2, numpy; print('All dependencies OK')"`

## 📈 System Status

### ✅ Completed Features
- [x] Binary visualization file format
- [x] Command-line recording integration (`-T` option)
- [x] Professional pygame visualizer
- [x] 64-character warrior name support
- [x] Interactive playback controls with speed adjustment
- [x] Memory grid visualization (80x100 for 8000 core)
- [x] Execution trail animation
- [x] Memory activity indicators
- [x] Battle statistics display
- [x] Warrior elimination tracking
- [x] Animated victory screens with particle effects
- [x] MP4 video recording with OpenCV
- [x] Headless mode for server deployment
- [x] Auto-speed calculation for target durations
- [x] Configurable appearance settings

### 🎯 Technical Specifications
- **File Format**: Binary `.viz` with 160-byte header
- **Memory Support**: Up to 8000 core locations (optimal grid: 80x100)
- **Name Length**: 64 characters per warrior
- **Event Types**: 10 different simulation events
- **Display**: Configurable grid layout with optimal sizing
- **Performance**: 60 FPS with configurable animation speed
- **Video Export**: MP4 format, 30-60 FPS, customizable quality
- **Speed Control**: 0.1 to 50,000 events per second

### 🎬 Video Features
- **Format**: MP4 with H.264 encoding
- **Quality**: 30-60 FPS, full HD resolution
- **Duration**: Auto-calculated or manual speed control
- **Effects**: Includes victory animations and particle effects
- **Deployment**: Headless mode for server-side generation

---

**Version**: CoreWar Visualizer v3.0
**Compatible With**: pMARS with visualization recording support
**Last Updated**: August 2025
**Status**: Production Ready with Video Export 🎬🚀

Enjoy visualizing and recording your CoreWar battles! 🎮⚔️🎬
