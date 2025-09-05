;name Sl2imp
;author Antoine Liu-Dujardin
;assert CORESIZE == 8000
spl 6; start the imp
spl 3; start second sleeper
slp #10, <-100 ;lazy bomb that will be scanned back
jmp -1, <-50 ;lazy bomb defending against imps
slp #10, <-2 ;scan back the bomb
jmp -1, <-3 ;scan back the bomb
mov 0, 1
