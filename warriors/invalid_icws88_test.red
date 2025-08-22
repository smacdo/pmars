;name Invalid ICWS 88 Test
;author Test
;strategy Test that invalid ICWS '88 features are rejected

start   MOV #1, #2     ; INVALID: immediate to immediate
        MUL $1, $2     ; INVALID: MUL not allowed in ICWS '88
        JMP #start     ; INVALID: immediate mode in JMP
        ADD.AB $1, $2  ; INVALID: modifiers not allowed
        MOV *1, $2     ; INVALID: * addressing mode not allowed
