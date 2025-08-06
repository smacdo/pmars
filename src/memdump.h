/* pMARS Memory Dump System Header
 * Function declarations for memory dumping functionality
 */

#ifndef MEMDUMP_H
#define MEMDUMP_H

/* Initialize memory dumping to specified file */
void init_memory_dump(const char* filename);

/* Dump current memory state and execution info */
void dump_memory_state(void);

/* Close memory dump file */
void close_memory_dump(void);

/* Check if memory dumping is enabled */
int is_dump_enabled(void);

/* Dump full memory state (for debugging or final state) */
void dump_full_memory(void);

#endif /* MEMDUMP_H */
