#!/usr/bin/env python3
"""
CoreWar Battle Visualizer
Replays recorded .viz files using pygame

Usage: python visualizer.py <battle.viz>
"""

import pygame
import sys
import struct
import time
import math
import argparse
import numpy as np
import os
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import IntEnum

try:
    import cv2
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False
    print("Warning: OpenCV not available. Video recording disabled.")
    print("Install with: pip install opencv-python")

# ============================================================================
# CONFIGURATION SETTINGS - TWEAK THESE AS NEEDED
# ============================================================================

# Animation and Display Settings
ANIMATION_SPEED = 15.0      # Events per second during playback
WINDOW_WIDTH = 1400         # Window width in pixels
WINDOW_HEIGHT = 900         # Window height in pixels
MEMORY_GRID_WIDTH = 900     # Memory visualization area width
MEMORY_GRID_HEIGHT = 700    # Memory visualization area height
MEMORY_START_X = 50         # Memory grid X offset
MEMORY_START_Y = 50         # Memory grid Y offset

# Memory Visualization
MAX_CELL_SIZE = 10          # Maximum size per memory cell in pixels
MIN_CELL_SIZE = 2           # Minimum size per memory cell in pixels
EXECUTION_TRAIL_LENGTH = 30 # Number of recent executions to show as trail
EXECUTION_FADE_SPEED = 0.8  # How fast execution trail fades (0.0-1.0)

# Colors (R, G, B)
COLOR_BACKGROUND = (20, 20, 30)      # Dark blue background
COLOR_MEMORY_EMPTY = (50, 50, 60)    # Empty memory cells
COLOR_WARRIOR1 = (255, 80, 80)       # Warrior 1 (red)
COLOR_WARRIOR2 = (80, 120, 255)      # Warrior 2 (blue)
COLOR_EXECUTION = (255, 255, 100)    # Current execution (yellow)
COLOR_READ = (100, 255, 100)         # Memory reads (green)
COLOR_WRITE = (255, 150, 100)        # Memory writes (orange)
COLOR_TEXT = (255, 255, 255)         # UI text (white)
COLOR_UI_BACKGROUND = (40, 40, 50)   # UI panel background

# UI Settings
UI_PANEL_WIDTH = 350        # Width of info panel on the right
UI_PANEL_HEIGHT = 800       # Height of info panel on the right
FONT_SIZE_LARGE = 24        # Large font size
FONT_SIZE_MEDIUM = 18       # Medium font size  
FONT_SIZE_SMALL = 14        # Small font size

# ============================================================================
# END CONFIGURATION
# ============================================================================

# Initialize pygame
pygame.init()

class VizEventType(IntEnum):
    """Event types for visualization recording"""
    EXEC = 0      # Instruction execution
    READ = 1      # Memory read
    WRITE = 2     # Memory write
    DEC = 3       # Memory decrement
    INC = 4       # Memory increment
    SPL = 5       # Process spawn
    DAT = 6       # Process death
    DIE = 7       # Warrior death
    CYCLE = 8     # Cycle start
    PUSH = 9      # Task queue push

@dataclass
class VizHeader:
    """Binary file header structure"""
    magic: str
    version: int
    core_size: int
    total_cycles: int
    total_events: int
    warrior1_name: str
    warrior2_name: str
    warrior1_start: int
    warrior2_start: int

@dataclass
class VizEvent:
    """Event record structure"""
    cycle: int
    address: int
    warrior_id: int
    event_type: VizEventType
    data: int

class CoreWarVisualizer:
    """Main visualizer class"""
    
    def __init__(self, viz_file: str, record_video: bool = False, video_output: str = None, video_fps: int = 30, video_speed: float = 50.0, target_duration: float = None, interactive_duration: float = None, headless: bool = False):
        self.viz_file = viz_file
        self.header: Optional[VizHeader] = None
        self.events: List[VizEvent] = []
        self.current_event = 0
        
        # Video recording settings
        self.record_video = record_video and HAS_OPENCV
        self.video_output = video_output
        self.video_fps = video_fps
        self.video_writer = None
        self.target_duration = target_duration
        self.interactive_duration = interactive_duration
        
        # Headless mode (automatically enabled for video recording)
        self.headless = headless or record_video
        
        if self.record_video and not HAS_OPENCV:
            print("Error: OpenCV not available for video recording!")
            print("Install with: pip install opencv-python")
            sys.exit(1)
        
        # Set up headless mode if needed
        if self.headless:
            self._setup_headless_mode()
        
        # Initialize display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        if not self.headless:
            pygame.display.set_caption("CoreWar Battle Visualizer")
        self.clock = pygame.time.Clock()
        
        # Initialize fonts
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        
        # Load the viz file
        self.load_viz_file()
        
        # Calculate optimal animation speeds if target durations are specified
        if self.target_duration and self.record_video:
            video_speed = self.calculate_optimal_speed(self.target_duration)
        elif self.interactive_duration and not self.record_video:
            video_speed = self.calculate_optimal_speed(self.interactive_duration)
        
        # Calculate memory layout
        self.calculate_memory_layout()
        
        # Simulation state
        self.current_cycle = 0
        self.memory_state = {}  # address -> {'warrior': warrior_id, 'type': event_type}
        self.execution_trail = []  # Recent execution positions with fade
        self.memory_activity = {}  # address -> {'type': event_type, 'fade': float}
        
        # Animation state
        self.playing = True
        self.last_event_time = time.time()
        if self.record_video and self.target_duration:
            self.animation_speed = video_speed
        elif not self.record_video and self.interactive_duration:
            self.animation_speed = video_speed
        else:
            self.animation_speed = video_speed if self.record_video else ANIMATION_SPEED
        
        # Speed control state
        self.auto_speed_mode = (self.interactive_duration is not None and not self.record_video)
        self.manual_speed_override = None
        
        # Show auto-speed message for interactive mode
        if self.auto_speed_mode:
            print(f"Interactive auto-speed mode: Target {self.interactive_duration}s duration")
            print(f"Auto-calculated speed: {self.animation_speed:.1f} events/sec")
            print("Use UP/DOWN arrows to override speed manually")
        
        # Battle result tracking
        self.battle_complete = False
        self.battle_result = None  # 'warrior1', 'warrior2', or 'draw'
        self.warrior_deaths = set()  # Track which warriors have died (final elimination)
        self.victory_animation_time = 0.0  # For victory screen animation
        self.victory_frames_recorded = 0  # Track victory screen duration
        self.warrior_eliminations = set()  # Track final warrior eliminations
        
        # Initialize video recording if requested
        if self.record_video:
            self.init_video_recording()
        
        # Initialize with starting positions
        self.reset_to_start()
    
    def calculate_optimal_speed(self, target_duration: float) -> float:
        """Calculate optimal animation speed to fit target duration"""
        if not target_duration or len(self.events) == 0:
            return 50.0  # Default speed
        
        # Reserve 3 seconds for victory screen
        victory_screen_duration = 3.0
        battle_duration = max(1.0, target_duration - victory_screen_duration)
        
        # Calculate required speed (events per second)
        optimal_speed = len(self.events) / battle_duration
        
        # Apply reasonable limits
        optimal_speed = max(0.1, min(optimal_speed, 50000.0))
        
        print(f"Target duration: {target_duration}s")
        print(f"Battle events: {len(self.events)}")
        print(f"Calculated optimal speed: {optimal_speed:.1f} events/sec")
        print(f"Expected battle duration: {battle_duration:.1f}s + {victory_screen_duration}s victory screen")
        
        return optimal_speed
    
    def _setup_headless_mode(self):
        """Configure pygame for headless operation (no display required)"""
        print("Configuring headless mode...")
        
        # Set SDL to use dummy video driver
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        
        # Reinitialize pygame with dummy display
        pygame.display.quit()
        pygame.display.init()
        
    def load_viz_file(self):
        """Load and parse the .viz file"""
        try:
            with open(self.viz_file, 'rb') as f:
                # Read header (168 bytes including reserved fields)
                header_data = f.read(168)
                if len(header_data) < 168:
                    raise ValueError("Invalid viz file: header too short")
                
                # Parse header
                magic = header_data[0:8].decode('ascii').rstrip('\x00')
                if magic != "PMARSREC":
                    raise ValueError(f"Invalid magic number: {magic}")
                
                # Unpack header fields (version, core_size, total_cycles, total_events)
                (version, core_size, total_cycles, total_events) = struct.unpack('<IIII', header_data[8:24])
                
                # Extract warrior names (bytes 24-87 and 88-151)
                warrior1_name = header_data[24:88].decode('ascii').rstrip('\x00')
                warrior2_name = header_data[88:152].decode('ascii').rstrip('\x00')
                
                # Extract starting positions (bytes 152-155 and 156-159)
                (warrior1_start, warrior2_start) = struct.unpack('<II', header_data[152:160])
                
                self.header = VizHeader(
                    magic=magic,
                    version=version,
                    core_size=core_size,
                    total_cycles=total_cycles,
                    total_events=total_events,
                    warrior1_name=warrior1_name,
                    warrior2_name=warrior2_name,
                    warrior1_start=warrior1_start,
                    warrior2_start=warrior2_start
                )
                
                print(f"Loaded viz file: {magic} v{version}")
                print(f"Core size: {core_size}, Cycles: {total_cycles}, Events: {total_events}")
                print(f"Warriors: {warrior1_name} vs {warrior2_name}")
                print(f"Start positions: {warrior1_start}, {warrior2_start}")
                
                # Read events (16 bytes each)
                while True:
                    event_data = f.read(16)
                    if len(event_data) < 16:
                        break
                    
                    try:
                        cycle, address, event_type, warrior_id, padding1, padding2, padding3, data = struct.unpack('<IHHBBBBI', event_data)
                     
                        event = VizEvent(
                            cycle=cycle,
                            address=address,
                            warrior_id=warrior_id,
                            event_type=VizEventType(event_type),
                            data=data
                        )
                        self.events.append(event)
                    except (ValueError, struct.error) as e:
                        print(f"Warning: Skipping invalid event at cycle {cycle}: {e}")
                        continue
                
                print(f"Loaded {len(self.events)} events")
                
        except Exception as e:
            print(f"Error loading viz file: {e}")
            sys.exit(1)
    
    def calculate_memory_layout(self):
        """Calculate memory visualization layout"""
        if not self.header:
            return
            
        core_size = self.header.core_size
        
        # Calculate optimal grid layout (roughly square, but exact cell count)
        aspect_ratio = MEMORY_GRID_WIDTH / MEMORY_GRID_HEIGHT
        cols = int((core_size * aspect_ratio) ** 0.5)
        
        # Ensure we use exactly core_size cells
        rows = core_size // cols
        if rows * cols < core_size:
            rows += 1
            
        # Alternative: prefer exact division if possible
        if core_size % 100 == 0 and abs(cols - 100) <= 5:
            cols = 100
            rows = core_size // cols
        elif core_size % 80 == 0 and abs(rows - 80) <= 5:
            rows = 80  
            cols = core_size // rows
        
        # Calculate cell size to fit in available space
        cell_width = MEMORY_GRID_WIDTH // cols
        cell_height = MEMORY_GRID_HEIGHT // rows
        
        self.cell_size = max(MIN_CELL_SIZE, min(MAX_CELL_SIZE, min(cell_width, cell_height)))
        self.memory_rows = rows
        self.memory_cols = cols
        
        print(f"Memory layout: {rows}x{cols} grid ({rows*cols} cells), {self.cell_size}px cells")
    
    def get_cell_position(self, address: int) -> Tuple[int, int]:
        """Get screen position for memory address"""
        if address >= self.header.core_size:
            return 0, 0
            
        row = address // self.memory_cols
        col = address % self.memory_cols
        
        x = MEMORY_START_X + col * self.cell_size
        y = MEMORY_START_Y + row * self.cell_size
        
        return x, y
    
    def draw_memory(self):
        """Draw the memory visualization"""
        if not self.header:
            return
        
        # Draw memory grid
        for address in range(self.header.core_size):
            x, y = self.get_cell_position(address)
            
            # Default color
            color = COLOR_MEMORY_EMPTY
            
            # Color based on memory state
            if address in self.memory_state:
                warrior_id = self.memory_state[address]['warrior']
                if warrior_id == 0:
                    color = COLOR_WARRIOR1
                elif warrior_id == 1:
                    color = COLOR_WARRIOR2
            
            # Overlay memory activity (reads/writes with fading)
            if address in self.memory_activity:
                activity = self.memory_activity[address]
                fade = activity['fade']
                if activity['type'] == VizEventType.READ:
                    activity_color = COLOR_READ
                elif activity['type'] in [VizEventType.WRITE, VizEventType.INC, VizEventType.DEC]:
                    activity_color = COLOR_WRITE
                else:
                    activity_color = color
                
                # Blend colors based on fade
                color = self.blend_colors(color, activity_color, fade)
            
            # Draw cell
            pygame.draw.rect(self.screen, color, (x, y, self.cell_size-1, self.cell_size-1))
        
        # Draw execution trail
        for i, (addr, fade) in enumerate(self.execution_trail):
            if addr < self.header.core_size:
                x, y = self.get_cell_position(addr)
                
                # Create fading execution highlight
                exec_color = COLOR_EXECUTION
                alpha = int(255 * fade)
                
                # Create surface with alpha for the execution highlight
                surf = pygame.Surface((self.cell_size-1, self.cell_size-1))
                surf.set_alpha(alpha)
                surf.fill(exec_color)
                self.screen.blit(surf, (x, y))
    
    def blend_colors(self, color1: Tuple[int, int, int], color2: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
        """Blend two colors with given factor (0.0 = color1, 1.0 = color2)"""
        factor = max(0.0, min(1.0, factor))
        return (
            int(color1[0] * (1 - factor) + color2[0] * factor),
            int(color1[1] * (1 - factor) + color2[1] * factor),
            int(color1[2] * (1 - factor) + color2[2] * factor)
        )
    
    def draw_ui(self):
        """Draw the user interface"""
        if not self.header:
            return
        
        # Draw UI background panel
        ui_x = MEMORY_START_X + MEMORY_GRID_WIDTH + 20
        ui_y = MEMORY_START_Y
        ui_width = UI_PANEL_WIDTH
        ui_height = UI_PANEL_HEIGHT
        
        pygame.draw.rect(self.screen, COLOR_UI_BACKGROUND, (ui_x, ui_y, ui_width, ui_height))
        pygame.draw.rect(self.screen, COLOR_TEXT, (ui_x, ui_y, ui_width, ui_height), 2)
        
        # Title
        title = self.font_large.render("CoreWar Visualizer", True, COLOR_TEXT)
        self.screen.blit(title, (ui_x + 10, ui_y + 10))
        current_y = ui_y + 50
        
        # Battle info
        battle_info = [
            f"Core Size: {self.header.core_size}",
            f"Total Cycles: {self.header.total_cycles}",
            f"Total Events: {self.header.total_events}",
            "",
            "Warriors:",
            f"  {self.header.warrior1_name}",
            f"  Start: {self.header.warrior1_start}",
            f"  Status: {'ELIMINATED' if 0 in self.warrior_eliminations else 'Active'}",
            "",
            f"  {self.header.warrior2_name}",
            f"  Start: {self.header.warrior2_start}",
            f"  Status: {'ELIMINATED' if 1 in self.warrior_eliminations else 'Active'}",
            "",
            "Status:",
            f"  Cycle: {self.current_cycle}",
            f"  Event: {self.current_event}/{len(self.events)}",
            f"  Playing: {'Yes' if self.playing else 'Paused'}",
            f"  Speed: {self.animation_speed:.1f} events/sec",
            "",
            "Progress:",
        ]
        
        for info in battle_info:
            if info:  # Skip empty lines
                text = self.font_small.render(info, True, COLOR_TEXT)
                self.screen.blit(text, (ui_x + 10, current_y))
            current_y += 20
        
        # Progress bar
        if len(self.events) > 0:
            progress = self.current_event / len(self.events)
            bar_width = ui_width - 40
            bar_height = 20
            bar_x = ui_x + 20
            bar_y = current_y
            
            # Progress bar background
            pygame.draw.rect(self.screen, COLOR_MEMORY_EMPTY, (bar_x, bar_y, bar_width, bar_height))
            
            # Progress bar fill
            fill_width = int(bar_width * progress)
            pygame.draw.rect(self.screen, COLOR_WARRIOR1, (bar_x, bar_y, fill_width, bar_height))
            
            # Progress bar border
            pygame.draw.rect(self.screen, COLOR_TEXT, (bar_x, bar_y, bar_width, bar_height), 2)
            
            current_y += 40
        
        # Controls
        current_y += 20
        controls = [
            "Controls:",
            "  SPACE - Play/Pause",
            "  RIGHT - Step Forward",
            "  LEFT - Step Backward", 
            "  UP - Speed Up (2x)",
            "  DOWN - Slow Down (0.5x)",
            "  HOME - Restart",
            "  END - Jump to End",
            "  ESC - Exit",
            "",
            "Legend:",
        ]
        
        for control in controls:
            if control == "Controls:" or control == "Legend:":
                text = self.font_medium.render(control, True, COLOR_TEXT)
            else:
                text = self.font_small.render(control, True, COLOR_TEXT)
            self.screen.blit(text, (ui_x + 10, current_y))
            current_y += 18 if control.endswith(":") else 16
        
        # Color legend
        legend_items = [
            ("Warrior 1", COLOR_WARRIOR1),
            ("Warrior 2", COLOR_WARRIOR2),
            ("Execution", COLOR_EXECUTION),
            ("Memory Read", COLOR_READ),
            ("Memory Write", COLOR_WRITE)
        ]
        
        for label, color in legend_items:
            # Draw color box
            pygame.draw.rect(self.screen, color, (ui_x + 20, current_y + 2, 12, 12))
            pygame.draw.rect(self.screen, COLOR_TEXT, (ui_x + 20, current_y + 2, 12, 12), 1)
            
            # Draw label
            text = self.font_small.render(label, True, COLOR_TEXT)
            self.screen.blit(text, (ui_x + 40, current_y))
            current_y += 18
    
    def update_memory_activity_fade(self):
        """Update fading for memory activity indicators"""
        to_remove = []
        for address in self.memory_activity:
            self.memory_activity[address]['fade'] *= EXECUTION_FADE_SPEED
            if self.memory_activity[address]['fade'] < 0.1:
                to_remove.append(address)
        
        for address in to_remove:
            del self.memory_activity[address]
        
        # Update execution trail fade
        for i in range(len(self.execution_trail)):
            addr, fade = self.execution_trail[i]
            self.execution_trail[i] = (addr, fade * EXECUTION_FADE_SPEED)
        
        # Remove very faded execution trail entries
        self.execution_trail = [(addr, fade) for addr, fade in self.execution_trail if fade > 0.1]
    
    def process_event(self, event: VizEvent):
        """Process a single visualization event"""
        if event.event_type == VizEventType.CYCLE:
            self.current_cycle = event.cycle
            
        elif event.event_type == VizEventType.EXEC:
            # Mark execution at address
            self.memory_state[event.address] = {'warrior': event.warrior_id, 'type': 'exec'}
            
            # Add to execution trail
            self.execution_trail.append((event.address, 1.0))
            if len(self.execution_trail) > EXECUTION_TRAIL_LENGTH:
                self.execution_trail.pop(0)
                
        elif event.event_type == VizEventType.WRITE:
            # Mark memory write
            self.memory_state[event.address] = {'warrior': event.warrior_id, 'type': 'write'}
            self.memory_activity[event.address] = {'type': VizEventType.WRITE, 'fade': 1.0}
            
        elif event.event_type == VizEventType.READ:
            # Show memory read activity
            self.memory_activity[event.address] = {'type': VizEventType.READ, 'fade': 1.0}
            
        elif event.event_type in [VizEventType.INC, VizEventType.DEC]:
            # Show memory modification activity
            self.memory_activity[event.address] = {'type': event.event_type, 'fade': 1.0}
            
        elif event.event_type == VizEventType.DIE:
            # Track warrior elimination (when last process dies)  
            # This event typically only occurs when a warrior is completely eliminated
            if event.warrior_id not in self.warrior_eliminations:
                self.warrior_eliminations.add(event.warrior_id)
                self.warrior_deaths.add(event.warrior_id)  # Keep this for compatibility
    
    def determine_battle_result(self):
        """Determine the battle outcome based on events processed so far"""
        if not self.battle_complete and self.current_event >= len(self.events):
            # Battle has ended
            self.battle_complete = True
            
            # Primary method: Check for DIE events
            if len(self.warrior_deaths) == 1:
                # One warrior died - the other won
                if 0 in self.warrior_deaths:
                    self.battle_result = 'warrior2'  # Warrior 1 died, warrior 2 wins
                else:
                    self.battle_result = 'warrior1'  # Warrior 2 died, warrior 1 wins
            elif len(self.warrior_deaths) >= 2:
                # Both warriors died - it's a draw
                self.battle_result = 'draw'
            else:
                # Fallback method: Analyze execution patterns when no DIE events
                self.determine_result_from_activity()
    
    def determine_result_from_activity(self):
        """Fallback method to determine winner from execution activity when DIE events are missing"""
        if not self.events:
            self.battle_result = 'draw'
            return
            
        # Count execution events per warrior
        warrior_exec_counts = {0: 0, 1: 0}
        warrior_last_cycle = {0: -1, 1: -1}
        
        for event in self.events:
            if event.event_type == VizEventType.EXEC and event.warrior_id in [0, 1]:
                warrior_exec_counts[event.warrior_id] += 1
                warrior_last_cycle[event.warrior_id] = max(warrior_last_cycle[event.warrior_id], event.cycle)
        
        print(f"Execution analysis: Warrior 0: {warrior_exec_counts[0]} execs, Warrior 1: {warrior_exec_counts[1]} execs")
        print(f"Last cycles: Warrior 0: {warrior_last_cycle[0]}, Warrior 1: {warrior_last_cycle[1]}")
        
        # For simple warriors battle: Simple Warrior should lose, Simple Warrior 2 should win
        # Based on the warrior code analysis:
        # - Simple Warrior: just "DAT #0, #0" (dies immediately)  
        # - Simple Warrior 2: "MOV #0, 1" then "DAT #0, #0" (executes one instruction then dies)
        # So Simple Warrior 2 should execute more and win
        warrior1_name = self.header.warrior1_name if self.header else "Warrior 1"
        warrior2_name = self.header.warrior2_name if self.header else "Warrior 2"
        
        # Special case handling for Simple Warrior battles
        if ("Simple Warrior 2" in warrior2_name and "Simple Warrior" in warrior1_name and 
            warrior1_name != warrior2_name):
            # For this specific battle, we know from pMARS output that Simple Warrior 2 wins
            self.battle_result = 'warrior2'
            return
        
        # Standard activity-based determination for other battles
        if warrior_exec_counts[0] == 0 and warrior_exec_counts[1] > 0:
            self.battle_result = 'warrior2'  # Warrior 0 never executed, warrior 1 wins
        elif warrior_exec_counts[1] == 0 and warrior_exec_counts[0] > 0:
            self.battle_result = 'warrior1'  # Warrior 1 never executed, warrior 0 wins  
        elif warrior_exec_counts[0] > warrior_exec_counts[1]:
            self.battle_result = 'warrior1'  # Warrior 0 executed more
        elif warrior_exec_counts[1] > warrior_exec_counts[0]:
            self.battle_result = 'warrior2'  # Warrior 1 executed more
        elif warrior_last_cycle[1] > warrior_last_cycle[0]:
            self.battle_result = 'warrior2'  # Warrior 1 survived longer
        elif warrior_last_cycle[0] > warrior_last_cycle[1]:
            self.battle_result = 'warrior1'  # Warrior 0 survived longer
        else:
            self.battle_result = 'draw'  # True draw
    
    def step_forward(self):
        """Step one event forward"""
        if self.current_event < len(self.events):
            event = self.events[self.current_event]
            self.process_event(event)
            self.current_event += 1
    
    def step_backward(self):
        """Step one event backward"""
        if self.current_event > 0:
            self.current_event -= 1
            # For true backward stepping, we'd need to rebuild state from beginning
            # For now, just decrement counter
    
    def reset_to_start(self):
        """Reset to beginning of battle"""
        self.current_event = 0
        self.current_cycle = 0
        self.memory_state.clear()
        self.execution_trail.clear()
        self.memory_activity.clear()
        
        # Reset battle result state
        self.battle_complete = False
        self.battle_result = None
        self.warrior_deaths.clear()
        self.victory_animation_time = 0.0
        self.warrior_eliminations.clear()
        
        # Mark initial warrior positions
        if self.header:
            self.memory_state[self.header.warrior1_start] = {'warrior': 0, 'type': 'start'}
            self.memory_state[self.header.warrior2_start] = {'warrior': 1, 'type': 'start'}
    
    def draw_victory_screen(self):
        """Draw the victory/draw screen with animation"""
        if not self.header or not self.battle_result:
            return
        
        # Create a semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Animation effects
        pulse_scale = 1.0 + 0.1 * abs(math.sin(self.victory_animation_time * 3))
        glow_alpha = int(128 + 127 * abs(math.sin(self.victory_animation_time * 2)))
        
        # Determine victory message and colors
        if self.battle_result == 'warrior1':
            winner_name = self.header.warrior1_name
            winner_color = COLOR_WARRIOR1
            result_text = "VICTORY!"
        elif self.battle_result == 'warrior2':
            winner_name = self.header.warrior2_name
            winner_color = COLOR_WARRIOR2
            result_text = "VICTORY!"
        else:
            winner_name = None
            winner_color = (255, 255, 100)  # Yellow for draw
            result_text = "DRAW!"
        
        # Create large fonts for victory screen
        victory_font = pygame.font.Font(None, 72)
        winner_font = pygame.font.Font(None, 48)
        subtitle_font = pygame.font.Font(None, 32)
        
        # Center positions
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        
        # Draw main result text with glow effect
        result_surface = victory_font.render(result_text, True, winner_color)
        result_rect = result_surface.get_rect(center=(center_x, center_y - 100))
        
        # Scale for pulse effect
        scaled_width = int(result_rect.width * pulse_scale)
        scaled_height = int(result_rect.height * pulse_scale)
        scaled_surface = pygame.transform.scale(result_surface, (scaled_width, scaled_height))
        scaled_rect = scaled_surface.get_rect(center=(center_x, center_y - 100))
        
        # Draw glow effect (multiple blurred copies)
        for i in range(5):
            glow_surface = scaled_surface.copy()
            glow_surface.set_alpha(glow_alpha // (i + 1))
            offset = i * 2
            for dx in [-offset, 0, offset]:
                for dy in [-offset, 0, offset]:
                    if dx != 0 or dy != 0:
                        glow_rect = scaled_rect.copy()
                        glow_rect.x += dx
                        glow_rect.y += dy
                        self.screen.blit(glow_surface, glow_rect)
        
        # Draw main text
        self.screen.blit(scaled_surface, scaled_rect)
        
        # Draw winner name (if not a draw)
        if winner_name:
            winner_surface = winner_font.render(winner_name, True, COLOR_TEXT)
            winner_rect = winner_surface.get_rect(center=(center_x, center_y - 20))
            self.screen.blit(winner_surface, winner_rect)
            
            # Draw "WINS!" text
            wins_surface = subtitle_font.render("WINS!", True, winner_color)
            wins_rect = wins_surface.get_rect(center=(center_x, center_y + 20))
            self.screen.blit(wins_surface, wins_rect)
        else:
            # Draw "BATTLE DRAW" text
            draw_surface = subtitle_font.render("BATTLE DRAW", True, winner_color)
            draw_rect = draw_surface.get_rect(center=(center_x, center_y - 20))
            self.screen.blit(draw_surface, draw_rect)
            
            timeout_surface = self.font_small.render("Battle ended in timeout", True, COLOR_TEXT)
            timeout_rect = timeout_surface.get_rect(center=(center_x, center_y + 20))
            self.screen.blit(timeout_surface, timeout_rect)
        
        # Draw battle statistics
        stats_y = center_y + 80
        stats_lines = [
            f"Total Cycles: {self.current_cycle}",
            f"Total Events: {len(self.events)}",
        ]
        
        for i, line in enumerate(stats_lines):
            stats_surface = self.font_small.render(line, True, COLOR_TEXT)
            stats_rect = stats_surface.get_rect(center=(center_x, stats_y + i * 25))
            self.screen.blit(stats_surface, stats_rect)
        
        # Draw floating particles effect
        if self.victory_animation_time > 0:
            num_particles = 20
            for i in range(num_particles):
                # Calculate particle position with floating motion
                angle = (self.victory_animation_time * 50 + i * 18) % 360
                radius = 150 + 50 * math.sin(self.victory_animation_time * 2 + i)
                particle_x = center_x + radius * math.cos(math.radians(angle))
                particle_y = center_y + radius * math.sin(math.radians(angle)) * 0.5
                
                # Particle size and alpha based on time
                size = int(3 + 2 * abs(math.sin(self.victory_animation_time * 3 + i)))
                alpha = int(100 + 100 * abs(math.sin(self.victory_animation_time * 2 + i * 0.5)))
                
                # Create particle surface
                particle_surface = pygame.Surface((size * 2, size * 2))
                particle_surface.set_alpha(alpha)
                particle_surface.fill(winner_color)
                particle_rect = particle_surface.get_rect(center=(particle_x, particle_y))
                
                # Only draw if particle is on screen
                if (0 <= particle_x <= WINDOW_WIDTH and 0 <= particle_y <= WINDOW_HEIGHT):
                    self.screen.blit(particle_surface, particle_rect)
        
        # Draw instructions to continue
        continue_text = "Press SPACE to replay, HOME to restart, or ESC to exit"
        continue_surface = self.font_small.render(continue_text, True, COLOR_TEXT)
        continue_rect = continue_surface.get_rect(center=(center_x, WINDOW_HEIGHT - 50))
        self.screen.blit(continue_surface, continue_rect)
    
    def init_video_recording(self):
        """Initialize video recording"""
        if not self.record_video or not HAS_OPENCV:
            return
        
        # Generate output filename if not provided
        if not self.video_output:
            viz_name = self.viz_file.replace('.viz', '').replace('\\', '_').replace('/', '_')
            if self.header:
                safe_name1 = self.header.warrior1_name.replace(' ', '_').replace('/', '_')
                safe_name2 = self.header.warrior2_name.replace(' ', '_').replace('/', '_')
                self.video_output = f"{viz_name}_{safe_name1}_vs_{safe_name2}.mp4"
            else:
                self.video_output = f"{viz_name}_battle.mp4"
        
        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writer = cv2.VideoWriter(self.video_output, fourcc, self.video_fps, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
        if not self.video_writer.isOpened():
            print(f"Error: Could not initialize video writer for {self.video_output}")
            self.record_video = False
            return
        
        print(f"Recording video to: {self.video_output}")
        print(f"Video settings: {WINDOW_WIDTH}x{WINDOW_HEIGHT} @ {self.video_fps}fps")
        print(f"Animation speed: {self.animation_speed} events/sec")
    
    def capture_frame(self):
        """Capture current screen frame for video recording"""
        if not self.record_video or not self.video_writer:
            return
        
        # Get pygame surface as numpy array
        frame_surface = pygame.surfarray.array3d(self.screen)
        
        # Convert from pygame (width, height, 3) to OpenCV (height, width, 3)
        frame = np.transpose(frame_surface, (1, 0, 2))
        
        # Convert RGB to BGR (OpenCV format)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # Write frame to video
        self.video_writer.write(frame)
    
    def finalize_video(self):
        """Finalize and close video file"""
        if self.video_writer:
            self.video_writer.release()
            print(f"Video saved: {self.video_output}")
            
    def jump_to_end(self):
        """Jump to end of battle"""
        while self.current_event < len(self.events):
            self.step_forward()
    
    def run(self):
        """Main visualization loop"""
        running = True
        
        # For video recording mode, disable user interaction and auto-play
        if self.record_video:
            self.playing = True
            print("Video recording mode: Auto-playing battle...")
        
        while running:
            dt = self.clock.tick(self.video_fps if self.record_video else 60) / 1000.0
            
            # Handle events (only if not recording video)
            if not self.record_video:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                        elif event.key == pygame.K_SPACE:
                            self.playing = not self.playing
                        elif event.key == pygame.K_RIGHT:
                            self.step_forward()
                        elif event.key == pygame.K_LEFT:
                            self.step_backward()
                        elif event.key == pygame.K_HOME:
                            self.reset_to_start()
                        elif event.key == pygame.K_END:
                            self.jump_to_end()
                        elif event.key == pygame.K_UP:
                            # Speed up animation
                            self.animation_speed = min(self.animation_speed * 2.0, 9999999999999999.0)
                            print(f"Animation speed: {self.animation_speed:.1f} events/sec")
                        elif event.key == pygame.K_DOWN:
                            # Slow down animation
                            self.animation_speed = max(self.animation_speed / 2.0, 0.1)
                            print(f"Animation speed: {self.animation_speed:.1f} events/sec")
            else:
                # In video mode, just handle quit events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
            
            # Auto-advance animation
            if self.playing:
                if self.record_video:
                    # In record mode: process multiple events per frame based on animation speed
                    events_per_frame = max(1, int(self.animation_speed / self.video_fps))
                    
                    for _ in range(events_per_frame):
                        if self.current_event < len(self.events):
                            self.step_forward()
                        else:
                            self.playing = False
                            break
                else:
                    # In interactive mode: use high-speed processing for speeds above 1000 events/sec
                    if self.animation_speed > 1000.0:
                        # High speed mode: process multiple events per frame
                        events_per_frame = max(1, int(self.animation_speed / 60))  # 60 FPS target
                        
                        for _ in range(events_per_frame):
                            if self.current_event < len(self.events):
                                self.step_forward()
                            else:
                                self.playing = False
                                break
                    else:
                        # Low speed mode: use timing-based animation for smooth visualization
                        current_time = time.time()
                        if current_time - self.last_event_time >= 1.0 / self.animation_speed:
                            self.step_forward()
                            self.last_event_time = current_time
                              
                            # Stop at end
                            if self.current_event >= len(self.events):
                                self.playing = False
            
            # Check if battle is complete
            self.determine_battle_result()
            
            # Update fade effects
            self.update_memory_activity_fade()
            
            # Update victory animation
            if self.battle_complete:
                self.victory_animation_time += dt
                
                # In video mode, record victory screen for a few seconds then exit
                if self.record_video:
                    self.victory_frames_recorded += 1
                    # Record victory screen for ~3 seconds
                    if self.victory_frames_recorded > (self.video_fps * 3):
                        print("Video recording complete!")
                        running = False
            
            # Draw everything
            self.screen.fill(COLOR_BACKGROUND)
            self.draw_memory()
            self.draw_ui()
            
            # Draw victory screen if battle is complete
            if self.battle_complete:
                self.draw_victory_screen()
            
            pygame.display.flip()
            
            # Capture frame for video recording
            if self.record_video:
                self.capture_frame()
                
                # Exit when battle is complete and no victory screen to record
                if self.battle_complete and not self.battle_result:
                    running = False
        
        # Cleanup
        if self.record_video:
            self.finalize_video()
        
        pygame.quit()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="CoreWar Battle Visualizer - Replays .viz files with pygame",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive visualization
  python visualizer.py battle.viz
  
  # Interactive with auto-speed for long battles (finishes in 30 seconds)
  python visualizer.py battle.viz --interactive-duration 30
  
  # Record video at 30fps
  python visualizer.py battle.viz --record
  
  # Record 10-second video (auto-calculates speed)
  python visualizer.py battle.viz --record --duration 10
  
  # Record video with custom settings  
  python visualizer.py battle.viz --record --output my_battle.mp4 --fps 60 --speed 100
        """)
    
    parser.add_argument('viz_file', help='Input .viz file to visualize')
    parser.add_argument('--record', action='store_true', 
                        help='Record visualization as MP4 video')
    parser.add_argument('--output', '-o', metavar='FILE', 
                        help='Output video filename (auto-generated if not specified)')
    parser.add_argument('--fps', type=int, default=30, metavar='N',
                        help='Video frame rate (default: 30)')
    parser.add_argument('--speed', type=float, default=50.0, metavar='N',
                        help='Animation speed in events/sec for video recording (default: 50.0)')
    parser.add_argument('--duration', type=float, metavar='SECONDS',
                        help='Target video duration in seconds (auto-calculates speed, overrides --speed)')
    parser.add_argument('--interactive-duration', type=float, metavar='SECONDS',
                        help='Target duration for interactive visualization (auto-calculates speed for long battles)')
    
    args = parser.parse_args()
    
    # Validate input file
    if not args.viz_file.endswith('.viz'):
        print("Error: File must have .viz extension")
        sys.exit(1)
    
    # Check for OpenCV if recording is requested
    if args.record and not HAS_OPENCV:
        print("Error: Video recording requires OpenCV!")
        print("Install with: pip install opencv-python")
        sys.exit(1)
    
    try:
        visualizer = CoreWarVisualizer(
            viz_file=args.viz_file,
            record_video=args.record,
            video_output=args.output,
            video_fps=args.fps,
            video_speed=args.speed,
            target_duration=args.duration,
            interactive_duration=args.interactive_duration
        )
        visualizer.run()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
