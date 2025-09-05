;name beta_1
;author Ian Ross
;assert CORESIZE == 8000

COPY_DIST EQU 2000

; Replicate ourself with new data
START
COPY_FWD MOV #COPY_DIST+1+SELF_R_JMP+3, START-1 ; Distance of copy (Pre-copy)
MOV #-COPY_DIST-5, <START-1; Self-copy'ers view of source pointer
JMP 3
COPY_BACK MOV #-COPY_DIST+SELF_R_JMP+1+6, START-1 ; Distance of copy (Pre-copy)
MOV #COPY_DIST-5, <START-1; Self-copy'ers view of source pointer
MAIN_COPY MOV #SELF_R-SELF_R_JMP-1, <START-1 ; Self-copyer's of dest pointer
MOV SELF_R+3, <START-1 ; copy Self R program
MOV SELF_R+2, <START-1 ; copy Self R program
MOV SELF_R+1, <START-1 ; copy Self R program
MOV SELF_R  , <START-1 ; copy Self R program
SPL @START-1
LOOP SLP #10
CMP COPY_DIST+SELF_R,SELF_R
JMP COPY_FWD
CMP -COPY_DIST+SELF_R,SELF_R
JMP COPY_BACK
MOV #-1,START-1
SLT #-1970, START-1
JMP LOOP
SLP #10
MOV SELF_R_JMP+1,<START-1
JMP -3

SELF_R MOV <SELF_R_JMP+2,<SELF_R_JMP+1 ; Offset to look back
CMP #-SELF_R_JMP-3+START, SELF_R_JMP+1 ; We always know the length to copy a-priori
JMP SELF_R,#0
SELF_R_JMP JMP LOOP, #0 ; Length of program + my own offset
END
