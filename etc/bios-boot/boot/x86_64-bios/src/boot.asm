section .bootloader_asm
bits 16

global _asm_start
extern _start

extern __load_start
extern __load_end
extern __mmap_start
extern __mmap_ct

extern __pt_start
extern __pt_end
extern __pt_lv4
extern __pt_lv3
extern __pt_lv2
extern __pt_lv1

%imacro print16 1
    mov si, %1
    call print_real
%endmacro

%imacro print16_halt 1
    print16 %1
    jmp halt
%endmacro

; =============================================
; stage one
;
; this section of the bootloader enters unreal
; mode, loads the second stage from disk,
; and jumps to the second stage.
; =============================================

_asm_start:                 ; beginning of bootloader code
    mov sp, 0x7c00          ; initialize stack

    mov [disk_num], dl      ; store disk number the bootloader is running from

    xor ax, ax              ; zero out segment registers
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax

    mov al, 0               ; clear screen
    mov ax, 3
    int 0x10

    print16 rmsg.stage_one  ; print info message

read_stage2:                ; read stage 2 bootloader
.check_ext:                 ; check that BIOS supports LBA
    mov ah, 0x41            ; set call parameters
    mov bx, 0x55aa
    mov dl, 0x80

    int 0x13                ; perform BIOS call
    jc .fail_ext            ; if carry bit set, fail

.read:                      ; perform read call
    mov eax, __load_start   ; calculate sectors to read
    mov ebx, __load_end
    sub ebx, eax            ; ebx = end - start
    shr ebx, 9              ; ebx >> 9 (ebx / 512)
    sub ebx, 1              ; ebx -= 1

    push ebx

    mov si, disk_pkt        ; load disk packet

.loop:
    pop ebx                 ; load remaining sectors
    cmp ebx, 0              ; check if done
    je .done

    sub ebx, 1              ; subtract 1 sector
    push ebx
    
    mov si, disk_pkt        ; load BIOS call values
    mov ah, 0x42
    mov dl, [disk_num]

    int 0x13                ; perform BIOS call
    jc .fail_read           ; if carry bit set, fail

    mov eax, [disk_pkt.offset]
    add eax, 0x200
    mov [disk_pkt.offset], eax

    mov eax, [disk_pkt.start]
    add eax, 1
    mov [disk_pkt.start], eax

    jmp .loop               ; read next sector

.fail_ext:
    print16_halt rmsg.noext

.fail_read:
    print16_halt rmsg.read_fail

.done:                      ; finish loading
    print16 rmsg.read_good
    jmp stage_two

; =============================================
; miscellaneous routines
;
; extra functions used throughout the
; bootloader
; =============================================

print_real:                 ; real mode print routine
    lodsb                   ; load next byte of message
    mov ah, 0x0e            ; set value for BIOS call
    cmp al, 0               ; if al == 0, we reached the null byte (terminator)
    je .end

    int 0x10                ; make BIOS call (print character)
    jmp print_real          ; next character

.end:                       ; finish the print routine
    mov al, 13              ; print \r
    int 0x10
    mov al, 10              ; print \n
    int 0x10
    ret                     ; return

halt:                       ; halt loop
    cli
    hlt
    jmp halt

; =============================================
; bootloader data
;
; this section is used to store various
; data used by the bootloader
; =============================================

disk_num:                   ; disk_num
    db 0x00                 ; stores number of disk the bootloader is on

disk_pkt:                   ; packet used for disk access calls
    db 0x10                 ; packet size (0x10, 16 bytes)
    db 0x00                 ; reserved
    .sectors: dw 0x01       ; amount of sectors to read
    .offset:  dw 0x7e00     ; where to place disk contents
    .segment: dw 0x00
    .start:   dd 0x01       ; starting sector
              dd 0x00

align 4
idt:                        ; null interrupt descriptor table
    .length: dw 0
    .base:   dd 0

gdt32:                      ; 32-bit global descriptor table
    .null:                  ; 8 null bytes
    dq 0x0

    .code:                  ; code descriptor
    dq 0xffff00000092cf00

    .data:                  ; data descriptor
    dq 0xffff00000092cf00

    .ptr:                   ; GDT pointer
    dw $-gdt32-1            ; limit
    dd gdt32                ; base address

gdt64:                      ; 64-bit global descriptor table
    .null:                  ; 8 null bytes
    dq 0x0

    .code:                  ; code descriptor
    dq 0x00209a0000000000

    .data:                  ; data descriptor
    dq 0x0000920000000000

    .ptr:                   ; GDT pointer
    dw $-gdt64-1            ; limit
    dd gdt64                ; base address

rmsg:                       ; bootloader info messages
    .stage_one:
    db "Starting bootloader.", 0
    .noext:
    db "Your BIOS does not support LBA addressing.", 0
    .read_fail:
    db "Failed to read stage 2 from disk.", 0
    .read_good:
    db "Read stage 2 from disk.", 0

pt:                         ; partition table
    times 0x1be-($-$$) db 0 ; pad to beginning
    .e1: times 2 dq 0       ; entry 1
    .e2: times 2 dq 0       ; entry 2
    .e3: times 2 dq 0       ; entry 3
    .e4: times 2 dq 0       ; entry 4

    dw 0xaa55               ; MBR magic signature

msg:                        ; bootloader info messages
    .stage_two:
    db "Entered stage 2.", 0
    .query_mmap:
    db "Querying memory map.", 0
    .mmap_fail:
    db "Failed to query BIOS for memory map.", 0
    .long_start:
    db "Preparing to enter long mode.", 0
    .fail_cpuid:
    db "Your CPU does not support CPUID.", 0
    .fail_long:
    db "Your CPU does not support long mode.", 0
    .no_active:
    db "No active partition found.", 0
    .found_part:
    db "Found active partition.", 0
    .read_fat:
    db "Read active partition.", 0

; =============================================
; stage two
;
; this section of the bootloader has to:
; - query higher memory maps (E820)
; - locate active partition
; - switch to unreal mode
; - copy partition to RAM
; - switch to protected => long mode
; - jump to rust code
; =============================================

stage_two:                  ; beginning of stage 2
    print16 msg.stage_two   ; print info message

mmap_query:                 ; query upper memory with E820
    print16 msg.query_mmap  ; print info message
    mov si, 0x1             ; set entry counter

    mov di, __mmap_start    ; buffer start
    mov eax, 0x0000e820     ; function opcode
    mov ebx, 0x0            ; clear ebx
    mov ecx, 24             ; buffer size
    mov edx, 0x534d4150     ; magic number
    int 0x15                ; BIOS call

    cmp eax, 0x534d4150     ; check for success
    jne .fail               ; eax != 0x534d4150 => fail
    jc .fail                ; carry bit set     => fail
    add di, 24              ; increment buf ptr

.call:
    mov eax, 0xe820         ; function opcode
    mov ecx, 24             ; struct size
    int 0x15                ; BIOS call
    add di, 24              ; increment buf ptr
    inc si                  ; increment entry counter

    cmp ebx, 0              ; check if end of list
    je .done                ; ebx == 0  => done
    jc .done                ; carry bit => done

    jmp .call               ; loop again

.fail:
    print16_halt msg.mmap_fail

.done:
    mov ebx, __mmap_ct      ; store entry count
    mov [ebx], si

unreal_mode:                ; enter unreal mode
    cli                     ; disable interrupts

    in al, 0x92             ; enable A20 line (fast A20)
    or al, 2
    out 0x92, al

    lgdt [gdt32.ptr]        ; load 32-bit GDT

    mov eax, cr0            ; enable protected mode
    or al, 1
    mov cr0, eax
    jmp .next

bits 32
.next:
    mov ax, 0x08            ; set data segment
    mov ds, ax

    mov eax, cr0            ; leave protected mode
    and al, 0xfe
    mov cr0, eax

bits 16
.unreal:
    sti                     ; reenable interrupts

get_active_part:            ; determine active partition
    xor ebx, ebx

    mov al, byte [pt.e1]    ; check partition 1
    shr al, 7
    cmp al, 1
    je .found
    add ebx, 2

    mov al, byte [pt.e2]    ; check partition 2
    shr al, 7
    cmp al, 1
    je .found
    add ebx, 2

    mov al, byte [pt.e3]    ; check partition 3
    shr al, 7
    cmp al, 1
    je .found
    add ebx, 2

    mov al, byte [pt.e4]    ; check partition 4
    shr al, 7
    cmp al, 1
    je .found

.fail:
    print16_halt msg.no_active

.found:                     ; found active partition
    print16 msg.found_part  ; print info message

    mov ecx, 0x200000       ; push buffer address
    push ecx

    ; sector count
    mov dword ecx, [0x7c00 + 0x1ca + ebx * 8]
    push ecx                ; push sector count

    ; partition start
    mov dword eax, [0x7c00 + 0x1c6 + ebx * 8]

    mov [disk_pkt.start], eax
    mov eax, 0x500
    mov [disk_pkt.offset], eax

read_active_part:           ; read active part. to 0x200000
    mov si, disk_pkt        ; load disk packet

.loop:
    pop ebx                 ; load remaining sectors
    cmp ebx, 0              ; check if done
    je .done

    sub ebx, 1              ; subtract 1 sector
    push ebx

    mov si, disk_pkt        ; load BIOS call values
    mov ah, 0x42
    mov dl, [disk_num]

    int 0x13                ; perform BIOS call
    jc .fail_read           ; if carry bit set, fail

    mov eax, [disk_pkt.start]
    add eax, 1
    mov [disk_pkt.start], eax

.mov_buffer:                ; move loaded sector to buffer
    pop ebx                 ; pop sector count
    pop edi                 ; pop load address
    push ebx                ; put sector count back

    mov esi, 0x500          ; source index = 0x500 (load buffer, see above)
    mov ecx, 0x80           ; operation count

.mov_loop:
    cmp ecx, 0              ; if moved all bytes, done
    je .mov_done

    mov dword eax, [esi]    ; load 4 bytes
    mov dword [edi], eax    ; store 4 bytes
    add edi, 4              ; increment edi and esi
    add esi, 4

    sub ecx, 1              ; decrement ecx
    jmp .mov_loop;

.mov_done:
    pop ebx                 ; pop sector count
    push edi                ; push new buffer address
    push ebx                ; put sector count back

    jmp .loop               ; read next sector

.fail_read:
    print16_halt rmsg.read_fail

.done:
    print16 msg.read_fat

; =============================================
; long mode
;
; here, we confirm the CPU is 64bit, setup our
; page table, enter long mode, and make
; the jump into rust code.
; =============================================

; https://wiki.osdev.org/Entering_Long_Mode_Directly
check_cpuid:                ; check to ensure the CPU supports CPUID
    pushfd                  ; push flags to eax register
    pop eax

    mov ecx, eax            ; ecx = flags
    xor eax, 0x200000       ; eax = flags ^ 0x200000
    push eax                ; flags ^= 0x200000
    popfd

    pushfd                  ; check if bit 21 is set
    pop eax
    xor eax, ecx
    shr eax, 21
    and eax, 1

    push ecx                ; put original cpu flags back
    popfd

    cmp eax, 0              ; eax == 0 => no CPUID
    je .fail_cpuid

    mov eax, 0x80000000     ; func: highest function implemented
    cpuid

    cmp eax, 0x80000001     ; check that extended proc info is supported
    jb .fail_cpuid

    jmp check_long

.fail_cpuid:
    print16_halt msg.fail_cpuid

check_long:                 ; check to ensure the CPU supports long mode
    mov eax, 0x80000001     ; func: extended processor features
    cpuid

    test edx, 1 << 29       ; test bit 29 (long mode)
    jz .fail_long           ; if not set, CPU does not support long mode

    jmp enter_long          ; prepare to enter long mode

.fail_long:
    print16_halt msg.fail_long

enter_long:                 ; prepare to enter long mode
    print16 msg.long_start  ; print info message

    mov edi, __pt_start     ; zero out page table buffer
    mov ecx, __pt_end
    sub ecx, edi            ; ecx = __pt_end - __pt_start
    shr ecx, 2              ; ecx >> 2 (ecx /= 4)
    xor eax, eax            ; eax = 0
    cld                     ; clear direction flag
    rep stosd               ; fill page table with zeros

create_page_table:          ; create page table
    %define PG_PRW 3        ; PRESENT | WRITE
    %define PG_HUGE 131     ; PRESENT | WRITE | SIZE

    mov eax, __pt_lv3       ; create page table level 4
    or eax, PG_PRW
    mov [__pt_lv4], eax

    mov eax, __pt_lv2       ; create page table level 3
    or eax, PG_PRW
    mov [__pt_lv3], eax

    mov ecx, 0              ; create page table level 2
    mov edi, __pt_lv2

.loop_page:                 ; loop over level 1 pages
    mov eax, 0x200000       ; 2 MB
    mul ecx                 ; eax *= ecx (page address)
    or eax, PG_HUGE         ; set page attributes

    mov [edi + ecx*8], eax  ; load page

    inc ecx                 ; increment counter
    cmp ecx, 512            ; check if done
    jne .loop_page

go_long:                    ; page table is ready
    cli                     ; disable interrupts

    mov ax, 0x10            ; set segment registers
    mov ss, ax

    mov al, 0xff            ; disable IRQs
    out 0xa1, al
    out 0x21, al

    lidt [idt]              ; load interrupt descriptor table
    mov eax, 0b00100000     ; set PAE and PGE
    mov cr4, eax

    mov eax, __pt_start     ; set page table pointer
    mov cr3, eax

    mov ecx, 0xc0000080     ; read feature MSR
    rdmsr
    or eax, 0x00000100      ; set LME (long mode enable) bit
    wrmsr

    mov ebx, cr0            ; enable paging and protected mode
    or ebx, 0x80000001
    mov cr0, ebx

    lgdt [gdt64.ptr]        ; load global descriptor table
    jmp 0x08:enter_rust     ; we are done!

bits 64
enter_rust:                 ; jump to Rust code, where we
    jmp _start              ; will load and run the kernel ELF
