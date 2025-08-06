;name Strategic Warrior
;author Test
;strategy Demonstrates SLP and ZAP instructions strategically

start   SLP #10       ; Sleep for 10 cycles (energy efficient timing)
        ZAP $50, #5   ; Zero out 5 memory locations starting 50 addresses ahead
        SLP #5        ; Sleep for 5 more cycles
        JMP start     ; Loop back to start
