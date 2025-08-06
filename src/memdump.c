/* pMARS Memory Dump System for Pygame Visualizer
 * This file provides functions to dump memory state and execution information
 * in JSON format for external visualization tools like pygame.
 */

#include "global.h"
#include "sim.h"
#include <stdio.h>
#include <string.h>
#include <time.h>

/* External variables from sim.c */
extern mem_struct FAR *memory;
extern warrior_struct *W;
extern ADDR_T progCnt;
extern long cycle;
extern int sim_round;
extern int warriorsLeft;
extern warrior_struct *endWar;

/* Global variables for memory dumping */
static FILE *dump_file = NULL;
static int dump_enabled = 0;
static int step_counter = 0;
static int first_dump = 1;

/* Opcode names for JSON output */
static const char* opcode_names[] = {
    "MOV", "ADD", "SUB", "MUL", "DIV", "MOD", "JMZ",
    "JMN", "DJN", "CMP", "SLT", "SPL", "DAT", "JMP",
    "SEQ", "SNE", "NOP", "LDP", "STP"
};

/* Modifier names for JSON output */
static const char* modifier_names[] = {
    "A", "B", "AB", "BA", "F", "X", "I"
};

/* Address mode names for JSON output */
static const char* addr_mode_names[] = {
    "IMMEDIATE", "DIRECT", "INDIRECT", "PREDECR", "POSTINC"
};

/* Initialize memory dumping */
void init_memory_dump(const char* filename) {
    if (filename && strlen(filename) > 0) {
        dump_file = fopen(filename, "w");
        if (dump_file) {
            dump_enabled = 1;
            step_counter = 0;
            first_dump = 1;
            
            /* Write JSON header */
            fprintf(dump_file, "{\n");
            fprintf(dump_file, "  \"simulation_info\": {\n");
            fprintf(dump_file, "    \"core_size\": %d,\n", coreSize);
            fprintf(dump_file, "    \"warriors\": %d,\n", warriors);
            fprintf(dump_file, "    \"max_cycles\": %ld,\n", cycles);
            fprintf(dump_file, "    \"rounds\": %d\n", rounds);
            fprintf(dump_file, "  },\n");
            fprintf(dump_file, "  \"warriors_info\": [\n");
            
            /* Dump warrior information */
            warrior_struct *war = warrior;
            for (int i = 0; i < warriors; i++) {
                fprintf(dump_file, "    {\n");
                fprintf(dump_file, "      \"id\": %d,\n", i);
                fprintf(dump_file, "      \"name\": \"%s\",\n", war->name ? war->name : "Unknown");
                fprintf(dump_file, "      \"author\": \"%s\",\n", war->authorName ? war->authorName : "Unknown");
                fprintf(dump_file, "      \"position\": %d,\n", war->position);
                fprintf(dump_file, "      \"length\": %d\n", war->instLen);
                fprintf(dump_file, "    }%s\n", (i < warriors - 1) ? "," : "");
                war++;
            }
            
            fprintf(dump_file, "  ],\n");
            fprintf(dump_file, "  \"execution_steps\": [\n");
            fflush(dump_file);
        }
    }
}

/* Dump current memory state and execution info */
void dump_memory_state(void) {
    if (!dump_enabled || !dump_file) return;
    
    /* Add comma separator for all but first dump */
    if (!first_dump) {
        fprintf(dump_file, ",\n");
    } else {
        first_dump = 0;
    }
    
    fprintf(dump_file, "    {\n");
    fprintf(dump_file, "      \"step\": %d,\n", step_counter++);
    fprintf(dump_file, "      \"round\": %d,\n", sim_round);
    fprintf(dump_file, "      \"cycle\": %ld,\n", cycle);
    fprintf(dump_file, "      \"warriors_left\": %d,\n", warriorsLeft);
    
    /* Current warrior information */
    if (W) {
        fprintf(dump_file, "      \"current_warrior\": {\n");
        fprintf(dump_file, "        \"id\": %d,\n", (int)(W - warrior));
        fprintf(dump_file, "        \"name\": \"%s\",\n", W->name ? W->name : "Unknown");
        fprintf(dump_file, "        \"pc\": %d,\n", progCnt);
        fprintf(dump_file, "        \"tasks\": %d\n", W->tasks);
        fprintf(dump_file, "      },\n");
    }
    
    /* Current instruction being executed */
    if (memory && progCnt < coreSize) {
        mem_struct *inst = &memory[progCnt];
        fprintf(dump_file, "      \"current_instruction\": {\n");
        fprintf(dump_file, "        \"address\": %d,\n", progCnt);
        fprintf(dump_file, "        \"opcode\": \"%s\",\n", 
                (inst->opcode < sizeof(opcode_names)/sizeof(opcode_names[0])) ? 
                opcode_names[inst->opcode] : "UNKNOWN");
        fprintf(dump_file, "        \"modifier\": \"%s\",\n", 
                modifier_names[0]); /* Default to A for now */
        fprintf(dump_file, "        \"a_mode\": \"%s\",\n", 
                (inst->A_mode < sizeof(addr_mode_names)/sizeof(addr_mode_names[0])) ?
                addr_mode_names[inst->A_mode] : "UNKNOWN");
        fprintf(dump_file, "        \"a_value\": %d,\n", inst->A_value);
        fprintf(dump_file, "        \"b_mode\": \"%s\",\n", 
                (inst->B_mode < sizeof(addr_mode_names)/sizeof(addr_mode_names[0])) ?
                addr_mode_names[inst->B_mode] : "UNKNOWN");
        fprintf(dump_file, "        \"b_value\": %d\n", inst->B_value);
        fprintf(dump_file, "      },\n");
    }
    
    /* Warrior states */
    fprintf(dump_file, "      \"warrior_states\": [\n");
    warrior_struct *war = warrior;
    for (int i = 0; i < warriors; i++) {
        fprintf(dump_file, "        {\n");
        fprintf(dump_file, "          \"id\": %d,\n", i);
        fprintf(dump_file, "          \"tasks\": %d,\n", war->tasks);
        fprintf(dump_file, "          \"position\": %d,\n", war->position);
        fprintf(dump_file, "          \"alive\": %s\n", (war->tasks > 0) ? "true" : "false");
        fprintf(dump_file, "        }%s\n", (i < warriors - 1) ? "," : "");
        war++;
    }
    fprintf(dump_file, "      ],\n");
    
    /* Memory dump - only dump changed or relevant areas to keep file size manageable */
    fprintf(dump_file, "      \"memory_changes\": [\n");
    
    /* For now, dump a window around the current PC and warrior positions */
    int dump_ranges[MAXWARRIOR * 2 + 2]; /* PC + warrior positions */
    int num_ranges = 0;
    
    /* Add current PC */
    if (progCnt < coreSize) {
        dump_ranges[num_ranges++] = progCnt;
    }
    
    /* Add warrior positions */
    war = warrior;
    for (int i = 0; i < warriors; i++) {
        if (war->tasks > 0) { /* Only alive warriors */
            dump_ranges[num_ranges++] = war->position;
        }
        war++;
    }
    
    /* Dump memory around these key locations */
    int first_mem = 1;
    for (int r = 0; r < num_ranges; r++) {
        int center = dump_ranges[r];
        int start = (center - 10 + coreSize) % coreSize;
        int end = (center + 10) % coreSize;
        
        for (int addr = start; addr != (end + 1) % coreSize; addr = (addr + 1) % coreSize) {
            if (addr >= 0 && addr < coreSize) {
                mem_struct *cell = &memory[addr];
                
                if (!first_mem) fprintf(dump_file, ",\n");
                first_mem = 0;
                
                fprintf(dump_file, "        {\n");
                fprintf(dump_file, "          \"address\": %d,\n", addr);
                fprintf(dump_file, "          \"opcode\": \"%s\",\n", 
                        (cell->opcode < sizeof(opcode_names)/sizeof(opcode_names[0])) ? 
                        opcode_names[cell->opcode] : "UNKNOWN");
                fprintf(dump_file, "          \"a_mode\": \"%s\",\n", 
                        (cell->A_mode < sizeof(addr_mode_names)/sizeof(addr_mode_names[0])) ?
                        addr_mode_names[cell->A_mode] : "UNKNOWN");
                fprintf(dump_file, "          \"a_value\": %d,\n", cell->A_value);
                fprintf(dump_file, "          \"b_mode\": \"%s\",\n", 
                        (cell->B_mode < sizeof(addr_mode_names)/sizeof(addr_mode_names[0])) ?
                        addr_mode_names[cell->B_mode] : "UNKNOWN");
                fprintf(dump_file, "          \"b_value\": %d,\n", cell->B_value);
                fprintf(dump_file, "          \"owner\": %d\n", 
                        (cell->debuginfo > 0 && cell->debuginfo <= warriors) ? 
                        cell->debuginfo - 1 : -1);
                fprintf(dump_file, "        }");
            }
        }
    }
    
    fprintf(dump_file, "\n      ]\n");
    fprintf(dump_file, "    }");
    
    fflush(dump_file);
}

/* Close memory dump file */
void close_memory_dump(void) {
    if (dump_enabled && dump_file) {
        fprintf(dump_file, "\n  ]\n");
        fprintf(dump_file, "}\n");
        fclose(dump_file);
        dump_file = NULL;
        dump_enabled = 0;
    }
}

/* Check if memory dumping is enabled */
int is_dump_enabled(void) {
    return dump_enabled;
}

/* Dump full memory state (for debugging or final state) */
void dump_full_memory(void) {
    if (!dump_enabled || !dump_file) return;
    
    fprintf(dump_file, "      \"full_memory\": [\n");
    
    for (int addr = 0; addr < coreSize; addr++) {
        mem_struct *cell = &memory[addr];
        
        fprintf(dump_file, "        {\n");
        fprintf(dump_file, "          \"address\": %d,\n", addr);
        fprintf(dump_file, "          \"opcode\": \"%s\",\n", 
                (cell->opcode < sizeof(opcode_names)/sizeof(opcode_names[0])) ? 
                opcode_names[cell->opcode] : "UNKNOWN");
        fprintf(dump_file, "          \"a_mode\": \"%s\",\n", 
                (cell->A_mode < sizeof(addr_mode_names)/sizeof(addr_mode_names[0])) ?
                addr_mode_names[cell->A_mode] : "UNKNOWN");
        fprintf(dump_file, "          \"a_value\": %d,\n", cell->A_value);
        fprintf(dump_file, "          \"b_mode\": \"%s\",\n", 
                (cell->B_mode < sizeof(addr_mode_names)/sizeof(addr_mode_names[0])) ?
                addr_mode_names[cell->B_mode] : "UNKNOWN");
        fprintf(dump_file, "          \"b_value\": %d,\n", cell->B_value);
        fprintf(dump_file, "          \"owner\": %d\n", 
                (cell->debuginfo > 0 && cell->debuginfo <= warriors) ? 
                cell->debuginfo - 1 : -1);
        fprintf(dump_file, "        }%s\n", (addr < coreSize - 1) ? "," : "");
    }
    
    fprintf(dump_file, "      ],\n");
    fflush(dump_file);
}
