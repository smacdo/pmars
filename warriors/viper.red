;redcode-94
;name Viper
;author AI Assistant
;strategy Advanced scanner/bomber with self-replicating capability
;assert CORESIZE == 8000

; Constants
STEP    equ 7
BOMB    equ (start+100)
DECOY   equ (start+50)

        org start

; Decoy area - looks like important code to confuse enemies
        for 10
        dat 0, 0
        rof

; Main scanner loop
start   mov bomb, ptr       ; prepare bomb
        add step, ptr       ; increment scan pointer
scan    cmp 0, @ptr         ; compare with target
        jmp found, 0        ; if different, we found enemy code
        cmp 1, @ptr         ; double-check next location
        jmp found, 0        ; if different, attack

        ; Continue scanning
        add step, ptr       ; next scan position
        jmp scan, 0         ; keep scanning

; Found enemy code - attack!
found   mov bomb, @ptr      ; drop bomb on enemy
        mov bomb, <ptr      ; bomb previous location too
        mov bomb, >ptr      ; bomb next location too

        ; Self-replicate for survival
        spl replicate, 0    ; split to create copy
        jmp start, 0        ; restart main loop

; Self-replication routine
replicate
        mov start, target   ; copy our code
        mov start+1, target+1
        mov start+2, target+2
        mov start+3, target+3
        mov start+4, target+4
        mov start+5, target+5
        jmp target, 0       ; jump to new copy

; Data section
ptr     dat #STEP, #0       ; scan pointer
bomb    dat #0, #0          ; bomb to drop
target  dat #2000, #0       ; replication target

        end start
