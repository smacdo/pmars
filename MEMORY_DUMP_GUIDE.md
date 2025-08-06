# pMARS Memory Dump System for Pygame Visualizer

This guide explains how to add memory dumping functionality to pMARS to create JSON output files that can be used with pygame or other visualization tools.

## What You Get

The memory dump system creates a JSON file containing:
- **Simulation metadata** (core size, warriors, cycles, rounds)
- **Warrior information** (names, authors, positions, lengths)
- **Step-by-step execution data** including:
  - Current warrior and program counter
  - Current instruction being executed
  - Memory state around active areas
  - Warrior states (alive/dead, task counts)

## Files Created

I've created the following files for you:

1. **`src/memdump.h`** - Header file with function declarations
2. **`src/memdump.c`** - Memory dumping implementation
3. **This guide** - Instructions for integration

## Integration Steps

### Step 1: Add Memory Dump to Build

You need to compile the memory dump functionality with pMARS. Add `memdump.c` to your build command:

```bash
# Basic build with memory dump support
gcc -O -DEXT94 -DPERMUTATE -DRWLIMIT -o pmars.exe pmars.c asm.c eval.c disasm.c cdb.c sim.c pos.c clparse.c global.c token.c str_eng.c memdump.c

# With graphics support
gcc -O -DEXT94 -DPERMUTATE -DRWLIMIT -DGRAPHX -DDOSTXTGRAPHX -o pmars.exe pmars.c asm.c eval.c disasm.c cdb.c sim.c pos.c clparse.c global.c token.c str_eng.c memdump.c
```

### Step 2: Add Command Line Option

To enable memory dumping, you'll need to add a command line option. Here's how to modify the code:

#### Option A: Simple Environment Variable Approach

Set an environment variable before running:
```bash
set PMARS_DUMP_FILE=battle_dump.json
pmars.exe warrior1.red warrior2.red
```

#### Option B: Command Line Flag (Requires Code Modification)

Add a new command line option like `-dump filename.json`.

### Step 3: Integration Points in sim.c

You need to add these calls to `sim.c` at key points:

```c
// At the top of sim.c, add:
#include "memdump.h"

// In simulator1() function, after memory allocation:
// Check for dump file environment variable or command line option
char* dump_filename = getenv("PMARS_DUMP_FILE");
if (dump_filename) {
    init_memory_dump(dump_filename);
}

// In the main execution loop, after each instruction execution:
// Add this call after the switch statement that executes instructions
if (is_dump_enabled()) {
    dump_memory_state();
}

// At the end of simulator1(), before cleanup:
close_memory_dump();
```

## JSON Output Format

The generated JSON file will look like this:

```json
{
  "simulation_info": {
    "core_size": 8000,
    "warriors": 2,
    "max_cycles": 80000,
    "rounds": 1
  },
  "warriors_info": [
    {
      "id": 0,
      "name": "Aeka",
      "author": "Unknown",
      "position": 0,
      "length": 7
    },
    {
      "id": 1,
      "name": "Flashpaper",
      "author": "Unknown",
      "position": 4000,
      "length": 5
    }
  ],
  "execution_steps": [
    {
      "step": 0,
      "round": 1,
      "cycle": 159998,
      "warriors_left": 2,
      "current_warrior": {
        "id": 0,
        "name": "Aeka",
        "pc": 2,
        "tasks": 1
      },
      "current_instruction": {
        "address": 2,
        "opcode": "MOV",
        "a_mode": "IMMEDIATE",
        "a_value": 0,
        "b_mode": "DIRECT",
        "b_value": 1
      },
      "warrior_states": [
        {
          "id": 0,
          "tasks": 1,
          "position": 0,
          "alive": true
        },
        {
          "id": 1,
          "tasks": 1,
          "position": 4000,
          "alive": true
        }
      ],
      "memory_changes": [
        {
          "address": 0,
          "opcode": "DAT",
          "a_mode": "DIRECT",
          "a_value": 0,
          "b_mode": "DIRECT",
          "b_value": 0,
          "owner": 0
        }
      ]
    }
  ]
}
```

## Using with Pygame

Here's a basic Python script to read and visualize the data:

```python
import json
import pygame
import sys

def load_battle_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def visualize_battle(data):
    pygame.init()

    # Setup display
    core_size = data['simulation_info']['core_size']
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Core War Visualizer")

    # Colors for different warriors
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

    clock = pygame.time.Clock()
    step = 0
    steps = data['execution_steps']

    running = True
    while running and step < len(steps):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    step += 1

        screen.fill((0, 0, 0))

        if step < len(steps):
            current_step = steps[step]

            # Draw memory state
            for mem in current_step['memory_changes']:
                addr = mem['address']
                owner = mem['owner']

                # Calculate position on screen
                x = (addr % 100) * 8
                y = (addr // 100) * 6

                if owner >= 0:
                    color = colors[owner % len(colors)]
                    pygame.draw.rect(screen, color, (x, y, 6, 4))

            # Draw current PC
            if 'current_warrior' in current_step:
                pc = current_step['current_warrior']['pc']
                x = (pc % 100) * 8
                y = (pc // 100) * 6
                pygame.draw.rect(screen, (255, 255, 255), (x-1, y-1, 8, 6), 2)

        pygame.display.flip()
        clock.tick(10)  # 10 FPS

    pygame.quit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python visualizer.py battle_dump.json")
        sys.exit(1)

    data = load_battle_data(sys.argv[1])
    visualize_battle(data)
```

## Quick Start Example

1. **Build pMARS with memory dump support:**
   ```bash
   gcc -O -DEXT94 -DPERMUTATE -DRWLIMIT -o pmars.exe pmars.c asm.c eval.c disasm.c cdb.c sim.c pos.c clparse.c global.c token.c str_eng.c memdump.c
   ```

2. **Run a battle with memory dumping:**
   ```bash
   set PMARS_DUMP_FILE=my_battle.json
   pmars.exe warriors\aeka.red warriors\flashpaper.red
   ```

3. **Visualize with pygame:**
   ```bash
   python visualizer.py my_battle.json
   ```

## Performance Considerations

- **File Size**: The JSON files can get large for long battles. The system only dumps memory around active areas to keep size manageable.
- **Performance Impact**: Memory dumping adds overhead. Use only when needed.
- **Frequency Control**: You can modify the dump frequency by adding conditions in the dump call.

## Customization Options

### Dump Frequency
Modify the dump call to only capture every N steps:
```c
static int dump_counter = 0;
if (is_dump_enabled() && (++dump_counter % 10 == 0)) {
    dump_memory_state();
}
```

### Memory Window Size
In `memdump.c`, change the window size around active areas:
```c
// Change from ±10 to ±20 addresses
int start = (center - 20 + coreSize) % coreSize;
int end = (center + 20) % coreSize;
```

### Additional Data
Add more information to the JSON by modifying the `dump_memory_state()` function in `memdump.c`.

## Troubleshooting

### Build Issues
- Make sure `memdump.c` is included in your gcc command
- Verify `memdump.h` is in the same directory as other headers

### Runtime Issues
- Check that the dump file path is writable
- Ensure sufficient disk space for large battles
- Verify JSON syntax with a validator if parsing fails

### Integration Issues
- Make sure to call `init_memory_dump()` before the simulation starts
- Call `close_memory_dump()` after the simulation ends
- Don't forget to include the header file in `sim.c`

## Next Steps

1. **Integrate the code** following the steps above
2. **Test with a simple battle** to verify JSON output
3. **Create your pygame visualizer** using the provided example
4. **Customize** the visualization to your needs

The memory dump system provides a solid foundation for creating sophisticated Core War visualizations. You can extend it to capture additional state information or modify the output format as needed for your specific visualization requirements.
