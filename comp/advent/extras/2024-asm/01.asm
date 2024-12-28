    global _start

; =============================

    section .bss

input_buffer:   resb 0x4000

left_list:      resd 1024
right_list:     resd 1024

left_list_ptr:  resq 1
right_list_ptr: resq 1

num_count:      resq 1

output_buffer:  resb 0x100

; =============================

    section .text

_start:
.read_input:
    mov rax, 0                          ; syscall id: read
    mov rdi, 0                          ;             fd (0 = stdin)
    mov rsi, input_buffer               ;             buffer
    mov rdx, 0x4000                     ;             buffer size
    syscall

    call parse_input                    ; parse input file

    mov rsi, left_list                  ; sort left list
    call sort_list

    mov rsi, right_list                 ; sort right list
    call sort_list

    call sum_p1                         ; calculate and print part 1 sum

.exit:
    mov rax, 60                         ; syscall id: exit
    mov rdi, 0                          ;             exit code
    syscall



; PARAMETERS:
;   none
parse_input:
    mov rsi, input_buffer               ; load input pointer
    mov rdi, left_list                  ; load left list pointer
    mov [left_list_ptr], rdi
    mov rdi, right_list                 ; load right list pointer
    mov [right_list_ptr], rdi

.start_left:
    xor rax, rax                        ; clear rax (accumulator)

.loop_left:
    movzx rbx, byte [rsi]               ; read 1 input byte
    inc rsi                             ; increment input pointer
    cmp rbx, 0x20                       ; check if byte is space
    je .finish_left                     ; if space, move on

    sub rbx, 0x30                       ; subtract ASCII '0'
    add rax, rax                        ; multiply rax by 10
    lea rax, [rax + 4 * rax]
    add rax, rbx                        ; add digit value to rax
    jmp .loop_left                      ; process next character

.finish_left:
    mov rdi, [left_list_ptr]            ; load left list pointer
    mov [rdi], eax                      ; write left number
    add rdi, 4                          ; advance left list pointer
    mov [left_list_ptr], rdi

.skip_whitespace:
    movzx rbx, byte [rsi]               ; read 1 input byte
    cmp rbx, 0x20                       ; check if byte is space
    jne .start_right                    ; if digit, parse right

    inc rsi                             ; increment input pointer
    jmp .skip_whitespace                ; process next character

.start_right:
    xor rax, rax                        ; clear rax (accumulator)

.loop_right:
    movzx rbx, byte [rsi]               ; read 1 input byte
    inc rsi                             ; increment input pointer
    cmp rbx, 0x0A                       ; check if byte is newline
    je .finish_right                    ; if newline, move on

    sub rbx, 0x30                       ; subtract ASCII '0'
    add rax, rax                        ; multiply rax by 10
    lea rax, [rax + 4 * rax]
    add rax, rbx                        ; add digit value to rax
    jmp .loop_right                     ; process next character

.finish_right:
    mov rdi, [right_list_ptr]           ; load right list pointer
    mov [rdi], eax                      ; write right number
    add rdi, 4                          ; advance right list pointer
    mov [right_list_ptr], rdi

    movzx rbx, byte [rsi+1]             ; read 1 input byte
    test rbx, rbx                       ; check if byte is 0 (null terminator)
    jnz .start_left                     ; if not 0, process next line

.calculate_num_count:
    mov rax, [left_list_ptr]            ; load left list pointer
    mov rbx, left_list                  ; load left list starting addr
    sub rax, rbx                        ; subtract two pointers
    shr rax, 2                          ; divide by 4
    mov [num_count], rax                ; store in num_count
    ret



; PARAMETERS:
;   rsi (list pointer)
sort_list:                              ; https://arxiv.org/pdf/2110.01111
    xor rcx, rcx                        ; zero counter 'i' (rcx)
    mov rdi, [num_count]                ; load number count

.loop_outer_start:
    xor rdx, rdx                        ; zero counter 'j' (rdx)

.loop_inner_start:
    mov eax, [rsi + 4 * rcx]            ; load element at position 'i' (rcx)
    mov ebx, [rsi + 4 * rdx]            ; load element at position 'j' (rdx)
    cmp eax, ebx                        ; compare elements at 'i' and 'j'
    jge .loop_inner_end                 ; if a[j] >= a[i], do not swap
    mov [rsi + 4 * rcx], ebx            ; swap a[i] and a[j]
    mov [rsi + 4 * rdx], eax

.loop_inner_end:
    inc rdx                             ; increment counter 'j' (rdx)
    cmp rdx, rdi                        ; compare j against list length
    jne .loop_inner_start               ; if not equal, continue

.loop_outer_end:
    inc rcx                             ; increment counter 'i' (rcx)
    cmp rcx, rdi                        ; compare i against list length
    jne .loop_outer_start               ; if not equal, continue
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
    call print_num
    ret



; PARAMETERS:
;   eax (number)
print_num:
    mov rdi, output_buffer              ; load output buffer pointer
    mov ecx, 10                         ; load division constant
    push rax                            ; save contents of eax

.find_length:
    xor edx, edx                        ; zero out upper 32 bits of dividend
    div ecx                             ; divide input number by power of 10
    test eax, eax                       ; test if quotient is zero (digit count found)
    jz .inner_start                     ; if zero, start printing loop
    imul ecx, 10                        ; multiply divisor by 10
    pop rax                             ; restore and save eax
    push rax
    jmp .find_length                    ; do another loop

.inner_start:
    mov eax, ecx                        ; move power of 10 divisor to eax
    xor edx, edx                        ; zero out upper 32 bits of dividend
    mov ebx, 10                         ; divide by 10 to get divisor for last digit
    div ebx
    mov ecx, eax                        ; store divisor in ecx

.print_digit:
    pop rax                             ; restore eax
    xor edx, edx                        ; zero out upper 32 bits of dividend
    div ecx                             ; divide input number by power of 10
    push rdx                            ; save remainder
    add eax, 0x30                       ; add ASCII '0'
    mov [rdi], al                       ; write byte to output
    inc rdi                             ; increment output pointer

    mov eax, ecx                        ; move power of 10 divisor to eax
    xor edx, edx                        ; zero out upper 32 bits of dividend
    mov ebx, 10                         ; divide by 10 to get divisor for next digit
    div ebx
    mov ecx, eax                        ; store divisor in ecx
    test ecx, ecx                       ; if divisor is zero (no more digits), end
    jz .end
    jmp .print_digit

.end:
    mov byte [rdi], 0x0A                ; write newline to output
    mov rdx, rdi                        ; calculate buffer size
    sub rdx, output_buffer
    add rdx, 1

    mov rax, 1                          ; syscall id: write
    mov rdi, 1                          ;             fd (1 = stdout)
    mov rsi, output_buffer              ;             buffer
    mov rdx, rdx                        ;             size
    syscall

    pop rax                             ; pop stored eax value
    ret
