;name ZAP Energy Test
;author Test
;strategy Test the exponential energy cost for ZAP instruction

start   ZAP $10, #1   ; Cost: 4 + 2^1 = 6 energy
        ZAP $20, #2   ; Cost: 4 + 2^2 = 8 energy
        ZAP $30, #3   ; Cost: 4 + 2^3 = 12 energy
        ZAP $40, #4   ; Cost: 4 + 2^4 = 20 energy
        ZAP $50, #5   ; Cost: 4 + 2^5 = 36 energy
        DAT #0, #0    ; End program
