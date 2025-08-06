/* pMARS Simulator with Memory Dump Integration
 * This file integrates memory dump functionality directly into the simulator
 */

#include "global.h"
#include "sim.h"
#include "memdump.h"
#include <time.h>
#include <unistd.h>
#include <stdlib.h>

/* Include the original simulator code but with memory dump integration */
#define ORIGINAL_SIMULATOR1
#include "sim.c"
#undef ORIGINAL_SIMULATOR1

/* Global variables for memory dump control */
static int dump_step_counter = 0;

/* Check for memory dump environment variable and initialize */
void check_and_init_dump() {
    char* dump_filename = getenv("PMARS_DUMP_FILE");
    if (dump_filename) {
        init_memory_dump(dump_filename);
        printf("Memory dumping enabled: %s\n", dump_filename);
    } else {
        printf("Memory dumping disabled (PMARS_DUMP_FILE not set)\n");
    }
}

/* Wrapper function that adds memory dump functionality */
void simulator1_with_dump() {
    /* Check for memory dump environment variable */
    check_and_init_dump();
    
    /* Call the original simulator with memory dump integration */
    simulator1();
    
    /* Close memory dump */
    close_memory_dump();
}

/* Override the original simulator1 function */
#ifdef ORIGINAL_SIMULATOR1
#undef simulator1
void simulator1() {
    simulator1_with_dump();
}
#endif
