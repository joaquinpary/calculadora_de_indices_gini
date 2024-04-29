section .data
    int_num dd 0

global asm_main
section .text

asm_main:
    push rbp
    mov rbp, rsp
    cvttss2si rax, xmm0
    inc rax
    mov rsp, rbp
    pop rbp
    ret
    