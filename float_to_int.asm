section .data
    int_num dd 0

global asm_main
section .text

asm_main:
    push ebp
    mov ebp, esp
    fld dword [esp + 8]
    fistp dword [int_num]
    mov eax, [int_num]
    inc eax
    mov esp, ebp
    pop ebp
    ret