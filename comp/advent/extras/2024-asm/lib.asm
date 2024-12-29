    global _start

; =============================

    section .bss

lib_read_input_buf: resb lib_read_input_buf_size
lib_read_input_buf_size equ 0x10000

lib_print_num_buf: resb lib_print_num_buf_size
lib_print_num_buf_size: equ 0x20

ASCII_newline equ 0x0A
ASCII_space equ " "
ASCII_minus equ "-"
ASCII_zero equ "0"
ASCII_nine equ "9"

SYS_read equ 0
SYS_write equ 1
SYS_exit equ 60

; =============================

    section .text

; Start function. Calls main from the solution assembly file.
_start:
    call lib_read_input                 ; read input file
    call main                           ; run solution

    xor rdi, rdi                        ; exit with code 0
    call lib_exit



; Calls exit(2) with the exit code in `rdi`.
lib_exit:
    mov rax, SYS_exit                   ; syscall id: exit
    syscall



; Reads input from standard input into `lib_read_input_buf`, with a maximum size
; of 64 kilobytes.
;
; If the data is too large for the buffer, then exit(0) is called.
lib_read_input:
    mov rax, SYS_read                   ; syscall id: read
    mov rdi, 0                          ;             fd (0 = stdin)
    mov rsi, lib_read_input_buf         ;             buffer
    mov rdx, lib_read_input_buf_size    ;             buffer size
    syscall

    cmp rax, lib_read_input_buf_size    ; compare return value to buffer size
    je .fail                            ; if equal (input too large), exit
    ret

.fail:
    mov rdi, 1                          ; exit with code 1
    call lib_exit



; Reads the number from the buffer at `rdi`, returning it in `rax`. A pointer to
; the first non-digit byte is returned in `rdx`.
lib_read_i64:
    xor rax, rax                        ; clear accumulator
    xor r9, r9                          ; clear r9 (minus flag)

    movzx r8, byte [rdi]                ; read byte from pointer
    cmp r8, ASCII_minus                 ; compare to minus
    jne .read_digit                     ; if not equal, start main loop

    mov r9, 1                           ; set r9 (minus flag)
    inc rdi                             ; increment input pointer

.read_digit:
    movzx r8, byte [rdi]                ; read byte from pointer
    inc rdi                             ; increment input pointer

    cmp r8, ASCII_zero                  ; compare to zero
    jl .end                             ; if less than, there are no more digits
    cmp r8, ASCII_nine                  ; compare to nine
    jg .end                             ; if greater than, there are no more digits

    sub r8, ASCII_zero                  ; subtract ASCII zero to get digit value
    imul rax, 10                        ; multiply accumulator by 10
    add rax, r8                         ; add digit value to accumulator

    jmp .read_digit                     ; read next digit (if any)

.end:
    mov rdx, rdi                        ; return pointer to byte past number end
    test r9, r9                         ; test r9 (minus flag)
    jnz .negate                         ; if negative, then negate the number
    ret

.negate:
    neg rax                             ; negate the number
    ret



; Skips over whitespace characters (spaces, newlines) from the buffer at `rdi`.
; Returns the pointer to the first non-whitespace character in `rax`.
lib_read_whitespace:
    mov al, byte [rdi]                  ; load byte from input
    cmp al, ASCII_space                 ; compare to space
    je .next
    cmp al, ASCII_newline               ; compare to newline
    je .next

    mov rax, rdi                        ; return pointer to non-whitespace
    ret

.next:
    inc rdi
    jmp lib_read_whitespace



; Prints the signed 64-bit integer stored in `rdi` out to standard output.
lib_print_i64:
    xor r8, r8                          ; clear r8 (minus flag)
    mov r9, 1

    test rdi, rdi                       ; test if number is negative
    cmovs r8, r9                        ; set r8 (minus flag) if negative

    mov rax, rdi                        ; move input number to rax
    mov rdi, lib_print_num_buf          ; store pointer to end of output buffer
    add rdi, lib_print_num_buf_size
    dec rdi

    mov byte [rdi], ASCII_newline       ; write newline character to end of output buffer
    dec rdi

    mov rcx, 10                         ; store constant divisor

.print_digit:
    cqo                                 ; sign extend dividend (rax)
    idiv rcx                            ; divide input number by 10
    add rdx, ASCII_zero                 ; add ASCII '0' to remainder (input % 10)
    mov byte [rdi], dl                  ; write digit character to output buffer
    dec rdi                             ; move output buffer pointer back
    test rax, rax                       ; test if quotient is zero
    jnz .print_digit                    ; if not zero, continue

.end:
    test r8, r8                         ; test minus flag
    jz .end_write                       ; if zero (positive), write
    mov byte [rdi], ASCII_minus         ; otherwise, write negative sign
    dec rdi

.end_write:
    inc rdi                             ; move forward (ignore undefined byte)

    mov rdx, lib_print_num_buf          ; calculate number of bytes to write
    add rdx, lib_print_num_buf_size

    mov rax, SYS_write                  ; syscall id: write
    sub rdx, rdi                        ;             size
    mov rsi, rdi                        ;             buffer
    mov rdi, 1                          ;             fd (1 = stdout)
    syscall

    ret

; Sorts the list of unsigned 32-bit numbers from `rdi` to `rsi`.
; Implementation: https://arxiv.org/pdf/2110.01111
;
; TODO: This is probably never a bottleneck
lib_sort_u32:
    mov r8, rdi                         ; store start pointer (r8)
    mov r9, rsi                         ; store end pointer (r9)

    xor r10, r10                        ; zero outer loop counter (r10)
    mov rsi, r8                         ; store outer list pointer in rsi

.loop_outer_start:
    mov rdi, r8                         ; store inner list pointer in rdi

.loop_inner:
    mov eax, [rsi]                      ; load number from outer list pointer
    mov edx, [rdi]                      ; load number from inner list pointer
    cmp eax, edx                        ; compare inner and outer elements
    jnl .loop_inner_end                 ; if !(inner < outer), move on

    mov [rsi], edx                      ; otherwise, swap inner and outer elements
    mov [rdi], eax

.loop_inner_end:
    add rdi, 4                          ; increment inner list pointer
    cmp rdi, r9                         ; compare to end pointer
    jne .loop_inner                     ; if not equal, continue

.loop_outer_end:
    add rsi, 4                          ; increment inner list pointer
    cmp rsi, r9                         ; compare to end pointer
    jne .loop_outer_start               ; if not equal, continue

    ret
