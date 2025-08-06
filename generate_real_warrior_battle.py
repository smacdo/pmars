#!/usr/bin/env python3
"""
Generate a 1000-step Core War battle JSON file using real warrior data
This creates a battle between Aeka and Rave warriors based on their actual code
"""

import json
import random
import math

def generate_real_warrior_battle():
    battle_data = {
        "simulation_info": {
            "core_size": 8000,
            "warriors": 2,
            "max_cycles": 1000,
            "rounds": 1
        },
        "warriors_info": [
            {
                "id": 0,
                "name": "Aeka",
                "author": "T.Hsu",
                "position": 0,
                "length": 100
            },
            {
                "id": 1,
                "name": "Rave",
                "author": "Stefan Strack", 
                "position": 4000,
                "length": 12
            }
        ],
        "execution_steps": []
    }
    
    # Aeka warrior instructions (suicidal stone & vector launched imp spiral)
    aeka_instructions = [
        {"opcode": "MOV", "a_mode": "IMMEDIATE", "a_value": 85, "b_mode": "IMMEDIATE", "b_value": 3504},
        {"opcode": "MOV", "a_mode": "IMMEDIATE", "a_value": 85, "b_mode": "IMMEDIATE", "b_value": 3494},
        {"opcode": "MOV", "a_mode": "PREDECR", "a_value": 12, "b_mode": "INDIRECT", "b_value": 10},
        {"opcode": "MOV", "a_mode": "PREDECR", "a_value": 11, "b_mode": "PREDECR", "b_value": 8},
        {"opcode": "SPL", "a_mode": "INDIRECT", "a_value": 5, "b_mode": "PREDECR", "b_value": -2856},
        {"opcode": "MOV", "a_mode": "PREDECR", "a_value": 7, "b_mode": "PREDECR", "b_value": 4},
        {"opcode": "SPL", "a_mode": "IMMEDIATE", "a_value": 1, "b_mode": "PREDECR", "b_value": -2856},
        {"opcode": "MOV", "a_mode": "IMMEDIATE", "a_value": 75, "b_mode": "PREDECR", "b_value": -10},
        {"opcode": "SPL", "a_mode": "PREDECR", "a_value": 0, "b_mode": "IMMEDIATE", "b_value": 87},
        {"opcode": "DJN", "a_mode": "INDIRECT", "a_value": 85, "b_mode": "IMMEDIATE", "b_value": 6},
        {"opcode": "MOV", "a_mode": "PREDECR", "a_value": 6, "b_mode": "IMMEDIATE", "b_value": 1},
        {"opcode": "SPL", "a_mode": "IMMEDIATE", "a_value": -1, "b_mode": "PREDECR", "b_value": -2857},
        {"opcode": "ADD", "a_mode": "IMMEDIATE", "a_value": 3, "b_mode": "IMMEDIATE", "b_value": -2},
        {"opcode": "DJN", "a_mode": "IMMEDIATE", "a_value": -2, "b_mode": "PREDECR", "b_value": -2859},
        {"opcode": "MOV", "a_mode": "IMMEDIATE", "a_value": 190, "b_mode": "PREDECR", "b_value": -190}
    ]
    
    # Rave warrior instructions (scanner/bomber)
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
    
    # Initialize battle state
    current_warrior = 0
    aeka_pc = 0
    rave_pc = 4001  # Rave starts at position 4000, first instruction at 4001
    aeka_tasks = 1
    rave_tasks = 1
    
    # Battle progression - Aeka is more aggressive with splitting
    battle_phase = 0  # 0=early, 1=middle, 2=late
    
    # Generate 1000 execution steps
    for step in range(1000):
        cycle = 1000 - step
        
        # Determine battle phase
        if step < 300:
            battle_phase = 0  # Early game
        elif step < 700:
            battle_phase = 1  # Middle game - most action
        else:
            battle_phase = 2  # Late game - one warrior should be winning
        
        # Determine warriors left
        if battle_phase < 2:
            warriors_left = 2
        else:
            # Late game - simulate Aeka winning (it's a strong warrior)
            if step > 850 and random.random() < 0.02:
                rave_tasks = max(0, rave_tasks - 1)
            warriors_left = 2 if rave_tasks > 0 else 1
        
        # Current warrior execution
        if current_warrior == 0:  # Aeka's turn
            pc = aeka_pc
            warrior_name = "Aeka"
            instruction = aeka_instructions[aeka_pc % len(aeka_instructions)]
            aeka_pc = (aeka_pc + 1) % len(aeka_instructions)
            
            # Aeka creates many processes through SPL instructions
            if instruction["opcode"] == "SPL" and battle_phase == 1:
                if aeka_tasks < 20 and random.random() < 0.3:
                    aeka_tasks += random.randint(1, 3)
            elif aeka_tasks > 1 and random.random() < 0.05:
                aeka_tasks -= 1
                
        else:  # Rave's turn
            pc = rave_pc
            warrior_name = "Rave"
            instruction = rave_instructions[(rave_pc - 4000) % len(rave_instructions)]
            rave_pc = 4000 + ((rave_pc - 4000 + 1) % len(rave_instructions))
            
            # Rave is more conservative with processes
            if instruction["opcode"] == "SPL" and battle_phase == 1:
                if rave_tasks < 8 and random.random() < 0.2:
                    rave_tasks += 1
            elif rave_tasks > 1 and random.random() < 0.03:
                rave_tasks -= 1
        
        # Ensure tasks don't go negative
        aeka_tasks = max(0, aeka_tasks)
        rave_tasks = max(0, rave_tasks)
        
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
                "tasks": aeka_tasks if current_warrior == 0 else rave_tasks
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
                    "tasks": aeka_tasks,
                    "position": 0,
                    "alive": aeka_tasks > 0
                },
                {
                    "id": 1,
                    "tasks": rave_tasks,
                    "position": 4000,
                    "alive": rave_tasks > 0
                }
            ],
            "memory_changes": []
        }
        
        # Add memory changes around current PC
        memory_range = 5 + battle_phase * 2  # More changes in later phases
        for i in range(-memory_range//2, memory_range//2 + 1):
            addr = (pc + i) % 8000
            
            # Determine ownership and instruction
            if addr < 100:  # Aeka area (length 100)
                owner = 0
                instr = aeka_instructions[addr % len(aeka_instructions)]
            elif addr >= 4000 and addr < 4012:  # Rave area (length 12)
                owner = 1
                instr = rave_instructions[(addr - 4000) % len(rave_instructions)]
            else:
                # Neutral area - might be affected by battle
                owner = -1
                if battle_phase > 0 and random.random() < 0.1:
                    # Battle effects - some instructions get overwritten
                    instr = {"opcode": "DAT", "a_mode": "IMMEDIATE", "a_value": 0, 
                            "b_mode": "IMMEDIATE", "b_value": 0}
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
        
        # Progress indicators
        if step % 200 == 0:
            print(f"Battle progress: Step {step}/1000, Aeka: {aeka_tasks} tasks, Rave: {rave_tasks} tasks")
    
    return battle_data

if __name__ == "__main__":
    print("Generating 1000-step battle: Aeka vs Rave...")
    print("Using real warrior instruction sets...")
    
    battle = generate_real_warrior_battle()
    
    with open("aeka_vs_rave_1000.json", "w") as f:
        json.dump(battle, f, indent=2)
    
    print("Generated aeka_vs_rave_1000.json with 1000 execution steps")
    print(f"File size: ~{len(json.dumps(battle)) // 1024} KB")
    print("Ready for visualization!")
