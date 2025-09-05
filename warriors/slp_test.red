;name SLP Test
;author Test
;strategy Test SLP instruction for low energy consumption
;assert CORESIZE == 8000

start   SLP #50        ; Sleep 50 cycles for only 1 energy
        MOV #1, 1      ; Simple instruction
        JMP start      ; Loop back
