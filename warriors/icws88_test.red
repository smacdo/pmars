;name ICWS 88 Test Warrior
;author Test
;strategy Test that only ICWS '88 instructions work
;assert CORESIZE == 8000

start   MOV #0, 1      ; Valid ICWS '88: immediate to direct
        ADD 1, 2       ; Valid ICWS '88: direct to direct
        JMP start      ; Valid ICWS '88: direct addressing
        DAT #0, #0     ; Valid ICWS '88: immediate mode in DAT
