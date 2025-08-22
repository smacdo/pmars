;name Random Fighter
;author Test
;strategy Somewhat unpredictable warrior for tournament testing
;assert CORESIZE == 8000

start   MOV #42, @5
        ADD #1, start
        JMP start+1
        SLP #10
        MOV #0, 2
        JMP start
