;name Test SLP and ZAP
;author Test
;strategy Test the new SLP and ZAP instructions

start   SLP #5      ; Sleep for 5 cycles (uses only 1 energy)
        ZAP $50, #3 ; Zero out 3 memory locations starting 50 addresses ahead
        DAT #0, #0  ; End program
