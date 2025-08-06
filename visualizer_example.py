#!/usr/bin/env python3
"""
pMARS Core War Visualizer Example
A simple pygame-based visualizer for pMARS memory dump files.

Usage: python visualizer_example.py battle_dump.json

Controls:
- SPACE: Next step
- LEFT/RIGHT: Navigate steps
- ESC/Q: Quit
- R: Reset to beginning
- F: Toggle fast mode
"""

import json
import pygame
import sys
import math

class CoreWarVisualizer:
    def __init__(self, data):
        self.data = data
        self.current_step = 0
        self.steps = data['execution_steps']
        self.core_size = data['simulation_info']['core_size']
        self.warriors = data['warriors_info']
        
        # Display settings
        self.width = 1000
        self.height = 800
        self.grid_size = int(math.sqrt(self.core_size))
        self.cell_size = min(self.width // self.grid_size, self.height // self.grid_size) - 1
        
        # Colors
        self.colors = {
            'background': (0, 0, 0),
            'empty': (20, 20, 20),
            'warrior_0': (255, 100, 100),
            'warrior_1': (100, 255, 100),
            'warrior_2': (100, 100, 255),
            'warrior_3': (255, 255, 100),
            'current_pc': (255, 255, 255),
            'text': (200, 200, 200),
            'ui_bg': (40, 40, 40)
        }
        
        # UI state
        self.fast_mode = False
        self.paused = False
        self.auto_play = True
        self.animation_speed = 10  # milliseconds between steps
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("pMARS Core War Visualizer")
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        self.clock = pygame.time.Clock()
    
    def get_cell_pos(self, address):
        """Convert memory address to screen coordinates"""
        row = address // self.grid_size
        col = address % self.grid_size
        x = col * (self.cell_size + 1) + 10
        y = row * (self.cell_size + 1) + 10
        return x, y
    
    def draw_memory(self):
        """Draw the core memory visualization"""
        if self.current_step >= len(self.steps):
            return
            
        step_data = self.steps[self.current_step]
        
        # Draw empty core
        for addr in range(self.core_size):
            x, y = self.get_cell_pos(addr)
            pygame.draw.rect(self.screen, self.colors['empty'], 
                           (x, y, self.cell_size, self.cell_size))
        
        # Draw memory with warrior ownership
        memory_map = {}
        for mem in step_data.get('memory_changes', []):
            memory_map[mem['address']] = mem
        
        for addr, mem in memory_map.items():
            x, y = self.get_cell_pos(addr)
            owner = mem.get('owner', -1)
            
            if owner >= 0:
                color_key = f'warrior_{owner}'
                color = self.colors.get(color_key, self.colors['warrior_0'])
                pygame.draw.rect(self.screen, color, 
                               (x, y, self.cell_size, self.cell_size))
        
        # Highlight current program counter
        if 'current_warrior' in step_data:
            pc = step_data['current_warrior']['pc']
            x, y = self.get_cell_pos(pc)
            pygame.draw.rect(self.screen, self.colors['current_pc'], 
                           (x-1, y-1, self.cell_size+2, self.cell_size+2), 2)
    
    def draw_ui(self):
        """Draw the user interface"""
        if self.current_step >= len(self.steps):
            return
            
        step_data = self.steps[self.current_step]
        
        # UI background
        ui_rect = pygame.Rect(self.width - 300, 0, 300, self.height)
        pygame.draw.rect(self.screen, self.colors['ui_bg'], ui_rect)
        
        y_offset = 20
        
        # Step information
        step_text = f"Step: {self.current_step + 1}/{len(self.steps)}"
        text_surf = self.font.render(step_text, True, self.colors['text'])
        self.screen.blit(text_surf, (self.width - 290, y_offset))
        y_offset += 30
        
        round_text = f"Round: {step_data.get('round', 1)}"
        text_surf = self.font.render(round_text, True, self.colors['text'])
        self.screen.blit(text_surf, (self.width - 290, y_offset))
        y_offset += 30
        
        cycle_text = f"Cycle: {step_data.get('cycle', 0)}"
        text_surf = self.font.render(cycle_text, True, self.colors['text'])
        self.screen.blit(text_surf, (self.width - 290, y_offset))
        y_offset += 30
        
        warriors_left = f"Warriors Left: {step_data.get('warriors_left', 0)}"
        text_surf = self.font.render(warriors_left, True, self.colors['text'])
        self.screen.blit(text_surf, (self.width - 290, y_offset))
        y_offset += 40
        
        # Current warrior info
        if 'current_warrior' in step_data:
            cw = step_data['current_warrior']
            warrior_text = f"Current Warrior:"
            text_surf = self.font.render(warrior_text, True, self.colors['text'])
            self.screen.blit(text_surf, (self.width - 290, y_offset))
            y_offset += 25
            
            name_text = f"  {cw.get('name', 'Unknown')}"
            text_surf = self.small_font.render(name_text, True, self.colors['text'])
            self.screen.blit(text_surf, (self.width - 290, y_offset))
            y_offset += 20
            
            pc_text = f"  PC: {cw.get('pc', 0)}"
            text_surf = self.small_font.render(pc_text, True, self.colors['text'])
            self.screen.blit(text_surf, (self.width - 290, y_offset))
            y_offset += 20
            
            tasks_text = f"  Tasks: {cw.get('tasks', 0)}"
            text_surf = self.small_font.render(tasks_text, True, self.colors['text'])
            self.screen.blit(text_surf, (self.width - 290, y_offset))
            y_offset += 30
        
        # Current instruction
        if 'current_instruction' in step_data:
            ci = step_data['current_instruction']
            inst_text = f"Current Instruction:"
            text_surf = self.font.render(inst_text, True, self.colors['text'])
            self.screen.blit(text_surf, (self.width - 290, y_offset))
            y_offset += 25
            
            opcode_text = f"  {ci.get('opcode', 'DAT')}"
            text_surf = self.small_font.render(opcode_text, True, self.colors['text'])
            self.screen.blit(text_surf, (self.width - 290, y_offset))
            y_offset += 20
            
            a_text = f"  A: {ci.get('a_mode', 'DIRECT')} {ci.get('a_value', 0)}"
            text_surf = self.small_font.render(a_text, True, self.colors['text'])
            self.screen.blit(text_surf, (self.width - 290, y_offset))
            y_offset += 20
            
            b_text = f"  B: {ci.get('b_mode', 'DIRECT')} {ci.get('b_value', 0)}"
            text_surf = self.small_font.render(b_text, True, self.colors['text'])
            self.screen.blit(text_surf, (self.width - 290, y_offset))
            y_offset += 30
        
        # Warrior states
        warrior_states_text = "Warrior States:"
        text_surf = self.font.render(warrior_states_text, True, self.colors['text'])
        self.screen.blit(text_surf, (self.width - 290, y_offset))
        y_offset += 25
        
        for i, warrior_state in enumerate(step_data.get('warrior_states', [])):
            warrior_info = self.warriors[i] if i < len(self.warriors) else {}
            name = warrior_info.get('name', f'Warrior {i}')
            alive = warrior_state.get('alive', False)
            tasks = warrior_state.get('tasks', 0)
            
            status = "ALIVE" if alive else "DEAD"
            color_key = f'warrior_{i}'
            color = self.colors.get(color_key, self.colors['text'])
            
            warrior_text = f"  {name}: {status} ({tasks})"
            text_surf = self.small_font.render(warrior_text, True, color)
            self.screen.blit(text_surf, (self.width - 290, y_offset))
            y_offset += 20
        
        # Controls
        y_offset = self.height - 150
        controls_text = "Controls:"
        text_surf = self.font.render(controls_text, True, self.colors['text'])
        self.screen.blit(text_surf, (self.width - 290, y_offset))
        y_offset += 25
        
        controls = [
            "SPACE: Next step",
            "LEFT/RIGHT: Navigate",
            "R: Reset",
            "F: Fast mode",
            "ESC/Q: Quit"
        ]
        
        for control in controls:
            text_surf = self.small_font.render(control, True, self.colors['text'])
            self.screen.blit(text_surf, (self.width - 290, y_offset))
            y_offset += 18
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    return False
                
                elif event.key == pygame.K_SPACE:
                    self.current_step = min(self.current_step + 1, len(self.steps) - 1)
                
                elif event.key == pygame.K_LEFT:
                    self.current_step = max(self.current_step - 1, 0)
                
                elif event.key == pygame.K_RIGHT:
                    self.current_step = min(self.current_step + 1, len(self.steps) - 1)
                
                elif event.key == pygame.K_r:
                    self.current_step = 0
                
                elif event.key == pygame.K_f:
                    self.fast_mode = not self.fast_mode
        
        return True
    
    def run(self):
        """Main visualization loop with game-like animation"""
        running = True
        last_step_time = pygame.time.get_ticks()
        
        print("🎮 Core War Battle Visualizer Started!")
        print("⚔️  Watch the warriors battle for control of the core!")
        print("🎯 Controls: SPACE=step, F=fast mode, R=reset, ESC=quit")
        print()
        
        while running:
            current_time = pygame.time.get_ticks()
            running = self.handle_events()
            
            # Auto-advance with animation timing
            if self.auto_play and not self.paused and self.current_step < len(self.steps) - 1:
                if current_time - last_step_time >= self.animation_speed:
                    self.current_step += 1
                    last_step_time = current_time
                    
                    # Print battle progress
                    if self.current_step % 10 == 0:
                        step_data = self.steps[self.current_step]
                        warriors_left = step_data.get('warriors_left', 0)
                        cycle = step_data.get('cycle', 0)
                        print(f"⚡ Step {self.current_step}: Cycle {cycle}, {warriors_left} warriors remaining")
            
            # Auto-advance in fast mode (overrides animation timing)
            elif self.fast_mode and self.current_step < len(self.steps) - 1:
                self.current_step += 1
                if self.current_step % 50 == 0:
                    step_data = self.steps[self.current_step]
                    warriors_left = step_data.get('warriors_left', 0)
                    print(f"🚀 Fast mode - Step {self.current_step}, {warriors_left} warriors left")
            
            # Check for battle end
            if self.current_step < len(self.steps):
                step_data = self.steps[self.current_step]
                warriors_left = step_data.get('warriors_left', 0)
                if warriors_left <= 1 and self.auto_play:
                    self.auto_play = False
                    self.paused = True
                    winner_id = -1
                    for i, state in enumerate(step_data.get('warrior_states', [])):
                        if state.get('alive', False):
                            winner_id = i
                            break
                    
                    if winner_id >= 0:
                        winner_name = self.warriors[winner_id]['name']
                        print(f"🏆 VICTORY! {winner_name} wins the battle!")
                    else:
                        print("🤝 Battle ended in a tie!")
            
            # Clear screen
            self.screen.fill(self.colors['background'])
            
            # Draw visualization
            self.draw_memory()
            self.draw_ui()
            
            # Update display
            pygame.display.flip()
            
            # Control frame rate
            if self.fast_mode:
                self.clock.tick(60)  # 60 FPS in fast mode
            else:
                self.clock.tick(30)  # 30 FPS normally for smooth animation
        
        print("👋 Thanks for watching the Core War battle!")
        pygame.quit()

def load_battle_data(filename):
    """Load battle data from JSON file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{filename}': {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python visualizer_example.py battle_dump.json")
        print("\nThis script visualizes pMARS Core War battles from JSON dump files.")
        print("Generate dump files by setting PMARS_DUMP_FILE environment variable")
        print("before running pMARS with the memory dump system integrated.")
        sys.exit(1)
    
    filename = sys.argv[1]
    print(f"Loading battle data from {filename}...")
    
    data = load_battle_data(filename)
    
    print(f"Loaded {len(data['execution_steps'])} execution steps")
    print(f"Core size: {data['simulation_info']['core_size']}")
    print(f"Warriors: {len(data['warriors_info'])}")
    
    for i, warrior in enumerate(data['warriors_info']):
        print(f"  {i}: {warrior['name']} by {warrior['author']}")
    
    print("\nStarting visualizer...")
    visualizer = CoreWarVisualizer(data)
    visualizer.run()

if __name__ == "__main__":
    main()
