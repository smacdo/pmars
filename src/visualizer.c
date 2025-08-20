/* pMARS Visualizer Module Implementation
 * Captures simulation events for replay visualization
 */

#include "visualizer.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

/* Global variables for visualization */
FILE *viz_file = NULL;        /* File handle for recording */
long viz_event_count = 0;     /* Number of events recorded */
static viz_header_t viz_header; /* File header */

/* Initialize visualization recording */
#ifdef NEW_STYLE
void viz_init(void)
#else
void viz_init()
#endif
{
    if (!SWITCH_R)
        return;

    viz_file = fopen(SWITCH_R, "wb");
    if (!viz_file) {
        errout("Error: Cannot open visualization file for writing\n");
        return;
    }

    /* Initialize header */
    memset(&viz_header, 0, sizeof(viz_header_t));
    strcpy(viz_header.magic, "PMARSREC");
    viz_header.version = 1;
    viz_header.core_size = coreSize;
    viz_header.total_cycles = cycles;
    viz_header.total_events = 0; /* Will be filled at close */

    /* Set warrior names and starting positions */
    if (warriors >= 1) {
        strncpy(viz_header.warrior1_name, warrior[0].name ? warrior[0].name : "Warrior1", 63);
        viz_header.warrior1_name[63] = '\0';
        viz_header.warrior1_start = warrior[0].position;
    }
    if (warriors >= 2) {
        strncpy(viz_header.warrior2_name, warrior[1].name ? warrior[1].name : "Warrior2", 63);
        viz_header.warrior2_name[63] = '\0';
        viz_header.warrior2_start = warrior[1].position;
    }
    /* Write header (will be updated at close) */
    fwrite(&viz_header, sizeof(viz_header_t), 1, viz_file);
    viz_event_count = 0;
}

/* Close visualization recording and update header */
#ifdef NEW_STYLE
void viz_close(void)
#else
void viz_close()
#endif
{
    if (!viz_file)
        return;

    /* Update header with final event count */
    viz_header.total_events = viz_event_count;
    
    /* Seek to beginning and rewrite header */
    fseek(viz_file, 0, SEEK_SET);
    fwrite(&viz_header, sizeof(viz_header_t), 1, viz_file);
    
    fclose(viz_file);
    viz_file = NULL;
}

/* Log a generic event */
#ifdef NEW_STYLE
void viz_log_event(viz_event_type_t type, int address, int warrior_id, uint32_t data)
#else
void viz_log_event(type, address, warrior_id, data)
viz_event_type_t type;
int address;
int warrior_id;
uint32_t data;
#endif
{
    viz_event_t event;
    
    if (!viz_file)
        return;

    event.cycle = cycle;
    event.address = (uint16_t)address;
    event.event_type = (uint16_t)type;
    event.warrior_id = (uint8_t)warrior_id;
    event.padding1 = 0;
    event.padding2 = 0;
    event.padding3 = 0;
    event.data = data;

    fwrite(&event, sizeof(viz_event_t), 1, viz_file);
    viz_event_count++;
}

/* Log instruction execution */
#ifdef NEW_STYLE
void viz_log_exec(int address)
#else
void viz_log_exec(address)
int address;
#endif
{
    int warrior_id = W - warrior; /* Current warrior index */
    uint32_t opcode = memory[address].opcode;
    viz_log_event(VIZ_EVENT_EXEC, address, warrior_id, opcode);
}

/* Log memory read */
#ifdef NEW_STYLE
void viz_log_read(int address)
#else
void viz_log_read(address)
int address;
#endif
{
    int warrior_id = W - warrior;
    viz_log_event(VIZ_EVENT_READ, address, warrior_id, 0);
}

/* Log memory write */
#ifdef NEW_STYLE
void viz_log_write(int address)
#else
void viz_log_write(address)
int address;
#endif
{
    int warrior_id = W - warrior;
    uint32_t value = (memory[address].A_value << 16) | memory[address].B_value;
    viz_log_event(VIZ_EVENT_WRITE, address, warrior_id, value);
}

/* Log memory decrement */
#ifdef NEW_STYLE
void viz_log_dec(int address)
#else
void viz_log_dec(address)
int address;
#endif
{
    int warrior_id = W - warrior;
    viz_log_event(VIZ_EVENT_DEC, address, warrior_id, 0);
}

/* Log memory increment */
#ifdef NEW_STYLE
void viz_log_inc(int address)
#else
void viz_log_inc(address)
int address;
#endif
{
    int warrior_id = W - warrior;
    viz_log_event(VIZ_EVENT_INC, address, warrior_id, 0);
}

/* Log process spawn (SPL instruction) */
#ifdef NEW_STYLE
void viz_log_spl(int warrior_id, int tasks)
#else
void viz_log_spl(warrior_id, tasks)
int warrior_id;
int tasks;
#endif
{
    viz_log_event(VIZ_EVENT_SPL, progCnt, warrior_id, tasks);
}

/* Log process death (DAT instruction) */
#ifdef NEW_STYLE
void viz_log_dat(int address, int warrior_id, int tasks)
#else
void viz_log_dat(address, warrior_id, tasks)
int address;
int warrior_id;
int tasks;
#endif
{
    viz_log_event(VIZ_EVENT_DAT, address, warrior_id, tasks);
}

/* Log warrior death */
#ifdef NEW_STYLE
void viz_log_die(int warrior_id)
#else
void viz_log_die(warrior_id)
int warrior_id;
#endif
{
    viz_log_event(VIZ_EVENT_DIE, 0, warrior_id, 0);
}

/* Log cycle start */
#ifdef NEW_STYLE
void viz_log_cycle(void)
#else
void viz_log_cycle()
#endif
{
    int warrior_id = W - warrior;
    viz_log_event(VIZ_EVENT_CYCLE, 0, warrior_id, cycle);
}

/* Log task queue push */
#ifdef NEW_STYLE
void viz_log_push(int value)
#else
void viz_log_push(value)
int value;
#endif
{
    int warrior_id = W - warrior;
    viz_log_event(VIZ_EVENT_PUSH, value, warrior_id, 0);
}
