/* This is a simple integration example showing where to add memory dump calls */

/* Add this include at the top of sim.c */
#include "memdump.h"
#include <stdlib.h>

/* Add this function to check for environment variable */
void check_and_init_dump() {
    char* dump_filename = getenv("PMARS_DUMP_FILE");
    if (dump_filename) {
        init_memory_dump(dump_filename);
        printf("Memory dumping enabled: %s\n", dump_filename);
    } else {
        printf("ERROOOOORRRR:::::::Memory dumping disabled\n");
    }
}

/* Add this call at the beginning of simulator1() function */
void simulator1_with_dump() {
    /* Check for memory dump environment variable */
    check_and_init_dump();
    
    /* ... rest of simulator1() code ... */
    
    /* Add this call in the main execution loop after instruction execution */
    /* This would go after the switch statement that executes instructions */
    if (is_dump_enabled()) {
        static int dump_counter = 0;
        /* Only dump every 10th step to keep file size manageable */
        if (++dump_counter % 10 == 0) {
            dump_memory_state();
        }
    }
    
    /* Add this call at the end before cleanup */
    close_memory_dump();
}
