;name ZAP Cost Test
;author Test
;strategy Test escalating ZAP energy costs
;assert CORESIZE == 8000

start   ZAP $10, #1    ; Cost: 4 + 2^1 = 6 energy
        ZAP $20, #2    ; Cost: 4 + 2^2 = 8 energy
        ZAP $30, #3    ; Cost: 4 + 2^3 = 12 energy
        MOV #1, 1      ; Low cost instruction to continue
        JMP start      ; Loop back
