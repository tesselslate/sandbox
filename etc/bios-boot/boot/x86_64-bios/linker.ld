ENTRY(_asm_start)

SECTIONS {
    /* bootloader asm */
    . = 0x7c00;
    
    __load_start = .;
    .bootloader_asm = .;

    /* rust bootloader code */
    .bootloader_rs : {
        *(.text .text.*)
        *(.rodata .rodata.*)
        *(.data .data.*)
        *(.bss .bss.*)
        *(.got)
    }

    /* pad disk image to nearest sector */
    .pad : {
        FILL(0x1234ABCD);
        . = ALIGN(512);
    }
    __load_end = .;

    /* E820 mmap storage markers */
    __mmap_start = .;
    . += 0x1000;
    __mmap_ct = .;
    . += 0x0010;
    
    /* page table storage markers */
    . = ALIGN(4096);
    __pt_start = .;

    __pt_lv4 = .;
    . += 0x1000;
    __pt_lv3 = .;
    . += 0x1000;
    __pt_lv2 = .;
    . += 0x1000;
    __pt_lv1 = .;
    . += 0x1000;

    __pt_end = .;
}
