;name Energy Test Warrior
;author Test
;strategy Demonstrate SLP and ZAP instructions with energy management

start   SLP #3, #0    ; Sleep for 3 cycles (uses only 1 energy)
        ZAP #0, #2    ; Zero out 2 memory locations (uses 3*2=6 energy)
        SLP #2, #0    ; Sleep for 2 more cycles (uses only 1 energy)
        DAT #0, #0    ; End program
