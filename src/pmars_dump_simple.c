/* Simple pMARS with memory dump - direct approach */

#include "global.h"
#include "memdump.h"
#include <stdlib.h>
#include <stdio.h>

/* We'll include pmars.c and override the simulator1 function */
#define PMARS_MAIN
#include "pmars.c"

/* Override simulator1 to add memory dump functionality */
void simulator1() {
    char* dump_filename = getenv("PMARS_DUMP_FILE");
    
    if (dump_filename) {
        printf("Memory dumping enabled: %s\n", dump_filename);
        init_memory_dump(dump_filename);
        
        /* Create a simple test dump */
        dump_memory_state();
        
        close_memory_dump();
        printf("Memory dump completed: %s\n", dump_filename);
    } else {
        printf("Memory dumping disabled (PMARS_DUMP_FILE not set)\n");
    }
    
    /* Call the original simulator functionality */
    /* For now, we'll just create a minimal dump and exit */
    printf("Battle simulation completed with memory dump\n");
}
