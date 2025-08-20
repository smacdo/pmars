/* pMARS Visualizer 
 * Binary file format for recording CoreWar battles for visualization replay
 */

#ifndef VISUALIZER_H
#define VISUALIZER_H

#include <stdint.h>
#include "global.h"

/* Event types for visualization recording */
typedef enum {
    VIZ_EVENT_EXEC = 0,     /* Instruction execution */
    VIZ_EVENT_READ = 1,     /* Memory read */
    VIZ_EVENT_WRITE = 2,    /* Memory write */
    VIZ_EVENT_DEC = 3,      /* Memory decrement */
    VIZ_EVENT_INC = 4,      /* Memory increment */
    VIZ_EVENT_SPL = 5,      /* Process spawn */
    VIZ_EVENT_DAT = 6,      /* Process death */
    VIZ_EVENT_DIE = 7,      /* Warrior death */
    VIZ_EVENT_CYCLE = 8,    /* Cycle start */
    VIZ_EVENT_PUSH = 9      /* Task queue push */
} viz_event_type_t;

/* Binary file header (160 bytes) */
typedef struct {
    char magic[8];           /* "PMARSREC" */
    uint32_t version;        /* Format version (1) */
    uint32_t core_size;      /* Memory size */
    uint32_t total_cycles;   /* Battle length */
    uint32_t total_events;   /* Number of events (filled at end) */
    char warrior1_name[64];  /* Warrior names (64 chars each) */
    char warrior2_name[64]; 
    uint32_t warrior1_start; /* Starting positions */
    uint32_t warrior2_start;
    uint32_t reserved[2];    /* Future use */
} viz_header_t;

/* Event record (16 bytes each) - properly aligned with uint16_t event_type */
typedef struct {
    uint32_t cycle;          /* Cycle number (4 bytes) */
    uint16_t address;        /* Memory address (2 bytes) */
    uint16_t event_type;     /* viz_event_type_t (2 bytes) */
    uint8_t warrior_id;      /* 0 or 1 (1 byte) */
    uint8_t padding1;        /* Padding byte (1 byte) */
    uint8_t padding2;        /* Padding byte (1 byte) */
    uint8_t padding3;        /* Padding byte (1 byte) */
    uint32_t data;           /* Context-specific data (4 bytes) */
} viz_event_t;               /* Total: 16 bytes */

/* Global variables */
extern FILE *viz_file;       /* File handle for recording */
extern long viz_event_count; /* Number of events recorded */

/* Function prototypes */
#ifdef NEW_STYLE
void viz_init(void);
void viz_close(void);
void viz_log_event(viz_event_type_t type, int address, int warrior_id, uint32_t data);
void viz_log_exec(int address);
void viz_log_read(int address);
void viz_log_write(int address);
void viz_log_dec(int address);
void viz_log_inc(int address);
void viz_log_spl(int warrior_id, int tasks);
void viz_log_dat(int address, int warrior_id, int tasks);
void viz_log_die(int warrior_id);
void viz_log_cycle(void);
void viz_log_push(int value);
#else
void viz_init();
void viz_close();
void viz_log_event();
void viz_log_exec();
void viz_log_read();
void viz_log_write();
void viz_log_dec();
void viz_log_inc();
void viz_log_spl();
void viz_log_dat();
void viz_log_die();
void viz_log_cycle();
void viz_log_push();
#endif

/* Macros for conditional logging */
#define VIZ_EXEC(addr)        do { if (SWITCH_R) viz_log_event(VIZ_EVENT_EXEC, addr, W - warrior, memory[addr].opcode); } while(0)
#define VIZ_READ(addr)        do { if (SWITCH_R) viz_log_event(VIZ_EVENT_READ, addr, W - warrior, 0); } while(0)
#define VIZ_WRITE(addr)       do { if (SWITCH_R) viz_log_event(VIZ_EVENT_WRITE, addr, W - warrior, (memory[addr].A_value << 16) | memory[addr].B_value); } while(0)
#define VIZ_DEC(addr)         do { if (SWITCH_R) viz_log_event(VIZ_EVENT_DEC, addr, W - warrior, 0); } while(0)
#define VIZ_INC(addr)         do { if (SWITCH_R) viz_log_event(VIZ_EVENT_INC, addr, W - warrior, 0); } while(0)
#define VIZ_SPL(wid, tasks)   do { if (SWITCH_R) viz_log_event(VIZ_EVENT_SPL, progCnt, wid, tasks); } while(0)
#define VIZ_DAT(addr, wid, tasks) do { if (SWITCH_R) viz_log_event(VIZ_EVENT_DAT, addr, wid, tasks); } while(0)
#define VIZ_DIE(wid)          do { if (SWITCH_R) viz_log_event(VIZ_EVENT_DIE, 0, wid, 0); } while(0)
#define VIZ_CYCLE()           do { if (SWITCH_R) viz_log_event(VIZ_EVENT_CYCLE, 0, W - warrior, cycle); } while(0)
#define VIZ_PUSH(val)         do { if (SWITCH_R) viz_log_event(VIZ_EVENT_PUSH, val, W - warrior, 0); } while(0)

#endif /* VISUALIZER_H */
