#!/usr/bin/env python3
"""
Generate a 100-step Core War battle JSON file for visualization
"""

import json
import random

def generate_battle_100():
    battle_data = {
        "simulation_info": {
            "core_size": 8000,
            "warriors": 2,
            "max_cycles": 100,
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
    
    # Rave warrior instructions (simplified)
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
    
    # Flash Paper instructions (simplified key ones)
    flash_instructions = [
        {"opcode": "SPL", "a_mode": "IMMEDIATE", "a_value": 89, "b_mode": "PREDECR", "b_value": -2050},
        {"opcode": "SPL", "a_mode": "IMMEDIATE", "a_value": 1, "b_mode": "PREDECR", "b_value": 440},
        {"opcode": "SPL", "a_mode": "IMMEDIATE", "a_value": 1, "b_mode": "PREDECR", "b_value": 460},
        {"opcode": "MOV", "a_mode": "IMMEDIATE", "a_value": 8, "b_mode": "IMMEDIATE", "b_value": 8},
        {"opcode": "MOV", "a_mode": "PREDECR", "a_value": -1, "b_mode": "PREDECR", "b_value": 2},
        {"opcode": "JMZ", "a_mode": "IMMEDIATE", "a_value": -5, "b_mode": "IMMEDIATE", "b_value": -5},
        {"opcode": "DAT", "a_mode": "IMMEDIATE", "a_value": 0, "b_mode": "IMMEDIATE", "b_value": 1}
    ]
    
    # Generate 100 execution steps
    current_warrior = 0
    rave_pc = 1
    flash_pc = 4000
    rave_tasks = 1
    flash_tasks = 8
    
    for step in range(100):
        cycle = 100 - step
        warriors_left = 2 if rave_tasks > 0 and flash_tasks > 0 else 1
        
        if current_warrior == 0:  # Rave's turn
            pc = rave_pc
            warrior_name = "Rave"
            instruction = rave_instructions[pc % len(rave_instructions)]
            rave_pc = (rave_pc + 1) % 12
            
            # Simulate some task changes
            if step % 20 == 0 and rave_tasks < 4:
                rave_tasks += 1
            elif step % 30 == 0 and rave_tasks > 1:
                rave_tasks -= 1
                
        else:  # Flash Paper's turn
            pc = flash_pc
            warrior_name = "Flash Paper3.7"
            instruction = flash_instructions[(flash_pc - 4000) % len(flash_instructions)]
            flash_pc = 4000 + ((flash_pc - 4000 + 1) % 100)
            
            # Simulate task changes for Flash Paper
            if step % 15 == 0 and flash_tasks < 12:
                flash_tasks += 1
            elif step % 25 == 0 and flash_tasks > 1:
                flash_tasks -= 1
        
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
        
        # Add some memory changes around current PC
        for i in range(-2, 3):
            addr = (pc + i) % 8000
            if addr < 12:  # Rave area
                owner = 0
                instr = rave_instructions[addr % len(rave_instructions)]
            elif addr >= 4000 and addr < 4100:  # Flash Paper area
                owner = 1
                instr = flash_instructions[(addr - 4000) % len(flash_instructions)]
            else:
                owner = -1
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
        
        # Simulate one warrior dying near the end
        if step > 80 and random.random() < 0.1:
            if rave_tasks > 0 and flash_tasks > 0:
                if random.random() < 0.5:
                    rave_tasks = 0
                else:
                    flash_tasks = 0
    
    return battle_data

if __name__ == "__main__":
    battle = generate_battle_100()
    with open("real_battle_100.json", "w") as f:
        json.dump(battle, f, indent=2)
    print("Generated real_battle_100.json with 100 execution steps")
