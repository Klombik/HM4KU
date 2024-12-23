# create_test_program.py
with open('test_program.asm', 'w', encoding='utf-8') as f:
    f.write("""
; test_program.asm
; Program for bitwise NOT operation on vector of length 8
; Vector starts at address 100

; Initialize registers
LOAD 0 0     ; R0 = 0 (counter)
LOAD 8 1     ; R1 = 8 (vector length)
LOAD 100 2   ; R2 = 100 (base address)

; Main loop
READ 2 3 0   ; Read vector element to R3
NOT 4 0 3    ; NOT operation, result to R4
WRITE 4 2    ; Write result back to memory

; Increment counter and check condition
LOAD 1 5     ; R5 = 1 (for increment)
READ 0 6 0   ; Read current counter
NOT 7 0 6    ; Invert for check
WRITE 7 0    ; Write back
""")