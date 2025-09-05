;name Energy System Test
;author Test
;strategy Test the new energy system with 80,000 initial energy and ZAP exponential costs
;assert CORESIZE == 8000

start   SLP #100      ; Sleep for 100 cycles (only 1 energy)
        ZAP $10, #1   ; Cost: 4 + 2^1 = 6 energy
        ZAP $20, #2   ; Cost: 4 + 2^2 = 8 energy
        ZAP $30, #3   ; Cost: 4 + 2^3 = 12 energy
        ZAP $40, #4   ; Cost: 4 + 2^4 = 20 energy
        ZAP $50, #5   ; Cost: 4 + 2^5 = 36 energy
        ZAP $60, #10  ; Cost: 4 + 2^10 = 1,028 energy (large zap!)
        DAT #0, #0    ; End program

; Total energy used: 1 + 6 + 8 + 12 + 20 + 36 + 1028 = 1,111 energy
; With 80,000 initial energy, warrior should complete all operations
