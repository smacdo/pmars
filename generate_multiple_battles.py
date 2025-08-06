#!/usr/bin/env python3
"""
Generate multiple Core War battles using different warrior combinations
Creates JSON files for each battle
"""

import json
import random
import os

def create_battle_template(warrior1_name, warrior2_name, steps=500):
    """Create a battle template with basic structure"""
    return {
        "simulation_info": {
            "core_size": 8000,
            "warriors": 2,
            "max_cycles": steps,
            "rounds": 1
        },
        "warriors_info": [
            {
                "id": 0,
                "name": warrior1_name,
                "author": "Generated",
                "position": 0,
                "length": 50
            },
            {
                "id": 1,
                "name": warrior2_name,
                "author": "Generated", 
                "position": 4000,
                "length": 50
            }
        ],
        "execution_steps": []
    }

def generate_simple_battle(warrior1, warrior2, steps=500):
    """Generate a simple battle between two warriors"""
    battle = create_battle_template(warrior1, warrior2, steps)
    
    # Simple instruction sets for demonstration
    instructions = [
        {"opcode": "MOV", "a_mode": "IMMEDIATE", "a_value": 0, "b_mode": "DIRECT", "b_value": 1},
        {"opcode": "ADD", "a_mode": "IMMEDIATE", "a_value": 1, "b_mode": "DIRECT", "b_value": -1},
        {"opcode": "JMP", "a_mode": "DIRECT", "a_value": -2, "b_mode": "DIRECT", "b_value": 0},
        {"opcode": "DAT", "a_mode": "IMMEDIATE", "a_value": 0, "b_mode": "IMMEDIATE", "b_value": 0},
        {"opcode": "SPL", "a_mode": "DIRECT", "a_value": 1, "b_mode": "DIRECT", "b_value": 0}
    ]
    
    current_warrior = 0
    pc = [0, 4000]
    tasks = [1, 1]
    
    for step in range(steps):
        cycle = steps - step
        warriors_left = sum(1 for t in tasks if t > 0)
        
        if warriors_left == 0:
            break
            
        # Skip if current warrior has no tasks
        if tasks[current_warrior] == 0:
            current_warrior = 1 - current_warrior
            continue
            
        # Get current instruction
        instr = instructions[step % len(instructions)]
        current_pc = pc[current_warrior]
        
        # Create execution step
        execution_step = {
            "step": step,
            "round": 1,
            "cycle": cycle,
            "warriors_left": warriors_left,
            "current_warrior": {
                "id": current_warrior,
                "name": warrior1 if current_warrior == 0 else warrior2,
                "pc": current_pc,
                "tasks": tasks[current_warrior]
            },
            "current_instruction": {
                "address": current_pc,
                "opcode": instr["opcode"],
                "modifier": "I",
                "a_mode": instr["a_mode"],
                "a_value": instr["a_value"],
                "b_mode": instr["b_mode"],
                "b_value": instr["b_value"]
            },
            "warrior_states": [
                {
                    "id": 0,
                    "tasks": tasks[0],
                    "position": 0,
                    "alive": tasks[0] > 0
                },
                {
                    "id": 1,
                    "tasks": tasks[1],
                    "position": 4000,
                    "alive": tasks[1] > 0
                }
            ],
            "memory_changes": []
        }
        
        # Add some memory changes
        for i in range(-2, 3):
            addr = (current_pc + i) % 8000
            memory_change = {
                "address": addr,
                "opcode": instr["opcode"],
                "a_mode": instr["a_mode"],
                "a_value": instr["a_value"],
                "b_mode": instr["b_mode"],
                "b_value": instr["b_value"],
                "owner": current_warrior if addr >= pc[current_warrior] and addr < pc[current_warrior] + 50 else -1
            }
            execution_step["memory_changes"].append(memory_change)
        
        battle["execution_steps"].append(execution_step)
        
        # Update state
        pc[current_warrior] = (pc[current_warrior] + 1) % 8000
        
        # Random task changes
        if instr["opcode"] == "SPL" and random.random() < 0.3:
            tasks[current_warrior] += 1
        elif random.random() < 0.05:
            tasks[current_warrior] = max(0, tasks[current_warrior] - 1)
            
        current_warrior = 1 - current_warrior
    
    return battle

def main():
    """Generate multiple battles"""
    warriors = ["hydra", "phoenix", "viper", "aeka", "rave", "flashpaper"]
    
    battles_to_generate = [
        ("hydra", "phoenix", 300),
        ("viper", "aeka", 400),
        ("rave", "flashpaper", 350),
        ("phoenix", "viper", 500),
        ("hydra", "rave", 450)
    ]
    
    print("Generating multiple warrior battles...")
    
    for warrior1, warrior2, steps in battles_to_generate:
        print(f"Creating battle: {warrior1} vs {warrior2} ({steps} steps)")
        
        battle = generate_simple_battle(warrior1, warrior2, steps)
        filename = f"{warrior1}_vs_{warrior2}_{steps}.json"
        
        with open(filename, "w") as f:
            json.dump(battle, f, indent=2)
        
        print(f"Generated {filename}")
    
    print(f"\nGenerated {len(battles_to_generate)} battle files!")
    print("Files created:")
    for warrior1, warrior2, steps in battles_to_generate:
        print(f"  - {warrior1}_vs_{warrior2}_{steps}.json")

if __name__ == "__main__":
    main()
