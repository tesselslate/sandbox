%include "lib.asm"

; =============================

    section .bss

left_list:      resd 1024
right_list:     resd 1024

num_count:      resq 1

output_buffer:  resb 0x100

; =============================

    section .text

main:

    call parse_input                    ; parse input file

    mov rdi, left_list                  ; sort left list
    mov rsi, left_list
    add rsi, 4*1000
    call lib_sort_u32

    mov rdi, right_list                 ; sort right list
    mov rsi, right_list
    add rsi, 4*1000
    call lib_sort_u32

    call sum_p1                         ; calculate and print part 1 sum
    call sum_p2                         ; calculate and print part 2 sum

    ret



; PARAMETERS:
;   none
parse_input:
    mov rdi, lib_read_input_buf         ; load input pointer
    mov r12, left_list                  ; load left list pointer
    mov r13, right_list                 ; load right list pointer

.read_line:
    call lib_read_i64                   ; parse left integer
    mov [r12], eax                      ; store into left list
    add r12, 4                          ; increment left list pointer
    mov rdi, rdx                        ; load post-int input pointer
    call lib_read_whitespace            ; skip spaces
    mov rdi, rax                        ; load post-whitespace input pointer

    call lib_read_i64                   ; parse right integer
    mov [r13], eax                      ; store into right list
    add r13, 4                          ; increment right list pointer
    mov rdi, rdx                        ; load post-int input pointer
    call lib_read_whitespace            ; skip newline
    mov rdi, rax                        ; load post-whitespace input pointer
    mov al, [rdi]                       ; load byte from input
    test al, al                         ; check for null terminator
    jnz .read_line                      ; if not null, continue
    jmp .end                            ; otherwise, end

.end:
    mov r13, left_list                  ; load left list start
    sub r12, r13                        ; subtract left list start from pointer
    shr r12, 2                          ; divide by 4
    mov [num_count], r12                ; store in num_count
    ret



; PARAMETERS:
;   none
sum_p1:
    xor rax, rax                        ; zero accumulator (rax)
    xor rcx, rcx                        ; zero counter (rcx)
    mov r8, [num_count]                 ; load num count
    mov r9, left_list                   ; load left list pointer
    mov r10, right_list                 ; load right list pointer

.loop_start:
    mov ebx, [r9]                       ; load left list number
    mov edx, [r10]                      ; load right list number

    sub ebx, edx                        ; subtract right from left
    cmp ebx, 0                          ; compare result to 0
    jge .loop_add                       ; if positive, add to sum
    sub eax, ebx                        ; otherwise, subtract to add to sum
    jmp .loop_end

.loop_add:
    add eax, ebx                        ; add to sum

.loop_end:
    add r9, 4                           ; advance left list pointer
    add r10, 4                          ; advance right list pointer

    inc rcx                             ; increment counter (rcx)
    cmp rcx, r8                         ; compare counter against list length
    jne .loop_start                     ; if not equal, continue

.print_result:
    mov rdi, rax
    call lib_print_i64
    ret



; PARAMETERS:
;   none
sum_p2:
    xor rax, rax                        ; zero accumulator (rax)
    xor rcx, rcx                        ; zero outer counter (rcx)
    mov r8, [num_count]                 ; load num count
    mov r9, left_list                   ; load left list pointer
    mov r11, right_list                 ; load right list pointer

.loop_outer:
    mov esi, [r9+4*rcx]                 ; load left list number
    xor rdx, rdx                        ; zero inner counter (rdx)

.loop_inner:
    mov edi, [r11+4*rdx]                ; load right list number
    cmp edi, esi                        ; compare right list number to left list number
    jg .loop_outer_end                  ; if greater, break; there are no more equal numbers
    jl .loop_inner_end                  ; if less than, go to the next loop iteration
    add eax, edi                        ; add left list number to rax

.loop_inner_end:
    inc rdx                             ; increment inner counter (rdx)
    cmp rdx, r8                         ; compare inner counter against list length
    jne .loop_inner                     ; if not equal, continue

.loop_outer_end:
    inc rcx                             ; increment outer counter (rcx)
    cmp rcx, r8                         ; compare outer counter against list length
    jne .loop_outer                     ; if not equal, continue

.print_result:
    mov rdi, rax
    call lib_print_i64
    ret
