#!/usr/bin/env python3
"""
Generate a 10,000-step Core War battle JSON file for visualization
This creates a realistic long-running battle between Rave and Flash Paper
"""

import json
import random
import math

def generate_battle_10000():
    battle_data = {
        "simulation_info": {
            "core_size": 8000,
            "warriors": 2,
            "max_cycles": 10000,
            "rounds": 1
        },
        "warriors_info": [
            {
                "id": 0,
                "name": "Rave",
                "author": "Stefan Strack",
                "position": 0,
                "length": 12
            },
            {
                "id": 1,
                "name": "Flash Paper3.7",
                "author": "Matt Hastings",
                "position": 4000,
                "length": 100
            }
        ],
        "execution_steps": []
    }
    
    # Rave warrior instructions (based on actual code)
    rave_instructions = [
        {"opcode": "SUB", "a_mode": "DIRECT", "a_value": 11, "b_mode": "IMMEDIATE", "b_value": 1},
        {"opcode": "CMP", "a_mode": "IMMEDIATE", "a_value": 125, "b_mode": "IMMEDIATE", "b_value": 113},
        {"opcode": "SLT", "a_mode": "IMMEDIATE", "a_value": 24, "b_mode": "IMMEDIATE", "b_value": -1},
        {"opcode": "DJN", "a_mode": "DIRECT", "a_value": -3, "b_mode": "PREDECR", "b_value": -308},
        {"opcode": "MOV", "a_mode": "IMMEDIATE", "a_value": 14, "b_mode": "IMMEDIATE", "b_value": 2},
        {"opcode": "MOV", "a_mode": "IMMEDIATE", "a_value": 4, "b_mode": "POSTINC", "b_value": -4},
        {"opcode": "DJN", "a_mode": "IMMEDIATE", "a_value": -1, "b_mode": "IMMEDIATE", "b_value": 0},
        {"opcode": "SUB", "a_mode": "IMMEDIATE", "a_value": 14, "b_mode": "IMMEDIATE", "b_value": -6},
        {"opcode": "JMN", "a_mode": "IMMEDIATE", "a_value": -8, "b_mode": "IMMEDIATE", "b_value": -8},
        {"opcode": "SPL", "a_mode": "IMMEDIATE", "a_value": 0, "b_mode": "IMMEDIATE", "b_value": 0},
        {"opcode": "MOV", "a_mode": "IMMEDIATE", "a_value": 1, "b_mode": "PREDECR", "b_value": -4},
        {"opcode": "DAT", "a_mode": "PREDECR", "a_value": -42, "b_mode": "PREDECR", "b_value": -42}
    ]
    
    # Flash Paper instructions (key strategic ones)
    flash_instructions = [
        {"opcode": "SPL", "a_mode": "IMMEDIATE", "a_value": 89, "b_mode": "PREDECR", "b_value": -2050},
        {"opcode": "SPL", "a_mode": "IMMEDIATE", "a_value": 1, "b_mode": "PREDECR", "b_value": 440},
        {"opcode": "SPL", "a_mode": "IMMEDIATE", "a_value": 1, "b_mode": "PREDECR", "b_value": 460},
        {"opcode": "SPL", "a_mode": "IMMEDIATE", "a_value": 17, "b_mode": "PREDECR", "b_value": 2113},
        {"opcode": "MOV", "a_mode": "IMMEDIATE", "a_value": 8, "b_mode": "IMMEDIATE", "b_value": 8},
        {"opcode": "MOV", "a_mode": "PREDECR", "a_value": -1, "b_mode": "PREDECR", "b_value": 2},
        {"opcode": "MOV", "a_mode": "PREDECR", "a_value": -2, "b_mode": "PREDECR", "b_value": 1},
        {"opcode": "SPL", "a_mode": "INDIRECT", "a_value": 0, "b_mode": "IMMEDIATE", "b_value": -2340},
        {"opcode": "MOV", "a_mode": "PREDECR", "a_value": -1, "b_mode": "PREDECR", "b_value": 1020},
        {"opcode": "JMZ", "a_mode": "IMMEDIATE", "a_value": -5, "b_mode": "IMMEDIATE", "b_value": -5},
        {"opcode": "MOV", "a_mode": "IMMEDIATE", "a_value": 0, "b_mode": "IMMEDIATE", "b_value": -1},
        {"opcode": "DAT", "a_mode": "IMMEDIATE", "a_value": 0, "b_mode": "IMMEDIATE", "b_value": 1}
    ]
    
    # Initialize battle state
    current_warrior = 0
    rave_pc = 1
    flash_pc = 4000
    rave_tasks = 1
    flash_tasks = 8
    
    # Battle progression parameters
    battle_intensity = 0.0  # Starts calm, builds up
    rave_aggression = 0.3
    flash_aggression = 0.7
    
    # Generate 10,000 execution steps with realistic battle progression
    for step in range(10000):
        cycle = 10000 - step
        
        # Calculate battle intensity (builds up over time, peaks in middle)
        battle_intensity = math.sin(step / 10000 * math.pi) * 0.8 + 0.2
        
        # Determine warriors left based on battle progression
        if step < 8000:
            warriors_left = 2  # Both alive for most of the battle
        elif step < 9500:
            # Gradual elimination phase
            if random.random() < 0.001 * battle_intensity:
                if rave_tasks > 0 and flash_tasks > 0:
                    if random.random() < 0.6:  # Flash Paper slightly more likely to survive
                        rave_tasks = max(0, rave_tasks - random.randint(1, 2))
                    else:
                        flash_tasks = max(0, flash_tasks - random.randint(1, 2))
            warriors_left = 2 if rave_tasks > 0 and flash_tasks > 0 else 1
        else:
            # Final phase - one warrior should be clearly winning
            warriors_left = 1 if step > 9800 else (2 if rave_tasks > 0 and flash_tasks > 0 else 1)
        
        # Current warrior logic
        if current_warrior == 0:  # Rave's turn
            pc = rave_pc
            warrior_name = "Rave"
            instruction = rave_instructions[pc % len(rave_instructions)]
            rave_pc = (rave_pc + 1) % 12
            
            # Dynamic task management for Rave
            if step % 50 == 0 and battle_intensity > 0.5:
                if rave_tasks < 6 and random.random() < rave_aggression:
                    rave_tasks += 1
                elif rave_tasks > 1 and random.random() < 0.1:
                    rave_tasks -= 1
                    
        else:  # Flash Paper's turn
            pc = flash_pc
            warrior_name = "Flash Paper3.7"
            instruction = flash_instructions[(flash_pc - 4000) % len(flash_instructions)]
            flash_pc = 4000 + ((flash_pc - 4000 + 1) % 100)
            
            # Dynamic task management for Flash Paper
            if step % 30 == 0:
                if flash_tasks < 15 and random.random() < flash_aggression * battle_intensity:
                    flash_tasks += random.randint(1, 2)
                elif flash_tasks > 2 and random.random() < 0.05:
                    flash_tasks -= 1
        
        # Ensure tasks don't go negative
        rave_tasks = max(0, rave_tasks)
        flash_tasks = max(0, flash_tasks)
        
        # Create execution step
        execution_step = {
            "step": step,
            "round": 1,
            "cycle": cycle,
            "warriors_left": warriors_left,
            "current_warrior": {
                "id": current_warrior,
                "name": warrior_name,
                "pc": pc,
                "tasks": rave_tasks if current_warrior == 0 else flash_tasks
            },
            "current_instruction": {
                "address": pc,
                "opcode": instruction["opcode"],
                "modifier": "I",
                "a_mode": instruction["a_mode"],
                "a_value": instruction["a_value"],
                "b_mode": instruction["b_mode"],
                "b_value": instruction["b_value"]
            },
            "warrior_states": [
                {
                    "id": 0,
                    "tasks": rave_tasks,
                    "position": 0,
                    "alive": rave_tasks > 0
                },
                {
                    "id": 1,
                    "tasks": flash_tasks,
                    "position": 4000,
                    "alive": flash_tasks > 0
                }
            ],
            "memory_changes": []
        }
        
        # Add memory changes around current PC with battle effects
        memory_range = min(8, int(3 + battle_intensity * 5))  # More changes during intense battle
        for i in range(-memory_range//2, memory_range//2 + 1):
            addr = (pc + i) % 8000
            
            # Determine ownership and instruction
            if addr < 12:  # Rave area
                owner = 0
                instr = rave_instructions[addr % len(rave_instructions)]
            elif addr >= 4000 and addr < 4100:  # Flash Paper area
                owner = 1
                instr = flash_instructions[(addr - 4000) % len(flash_instructions)]
            else:
                # Neutral area - might be affected by battle
                owner = -1
                if random.random() < battle_intensity * 0.1:
                    # Battle debris - corrupted instructions
                    instr = {"opcode": "DAT", "a_mode": "IMMEDIATE", "a_value": random.randint(0, 100), 
                            "b_mode": "IMMEDIATE", "b_value": random.randint(0, 100)}
                else:
                    instr = {"opcode": "DAT", "a_mode": "DIRECT", "a_value": 0, "b_mode": "DIRECT", "b_value": 0}
            
            memory_change = {
                "address": addr,
                "opcode": instr["opcode"],
                "a_mode": instr["a_mode"],
                "a_value": instr["a_value"],
                "b_mode": instr["b_mode"],
                "b_value": instr["b_value"],
                "owner": owner
            }
            execution_step["memory_changes"].append(memory_change)
        
        battle_data["execution_steps"].append(execution_step)
        
        # Alternate warriors
        current_warrior = 1 - current_warrior
        
        # Add some dramatic moments
        if step in [2500, 5000, 7500, 9000, 9500]:
            print(f"Battle milestone: Step {step}, Rave: {rave_tasks} tasks, Flash: {flash_tasks} tasks, Intensity: {battle_intensity:.2f}")
    
    return battle_data

if __name__ == "__main__":
    print("Generating epic 10,000-step Core War battle...")
    print("This may take a moment...")
    
    battle = generate_battle_10000()
    
    with open("real_battle_10000.json", "w") as f:
        json.dump(battle, f, indent=2)
    
    print("Generated real_battle_10000.json with 10,000 execution steps")
    print(f"File size: ~{len(json.dumps(battle)) // 1024} KB")
    print("Ready for epic visualization!")
