use core::arch::asm;

/// Receives a byte of input from the given port
/// using the x86 "in" instruction.
#[inline(always)]
pub unsafe fn read(port: u16) -> u8 {
    let byte: u8;

    asm!(
        "in al, dx",
        out("al") byte,
        in("dx") port
    );

    byte
}

/// Outputs a byte to the given port using the 
/// x86 "out" instruction.
#[inline(always)]
pub unsafe fn write(port: u16, byte: u8) {
    asm!(
        "out dx, al",
        in("dx") port,
        in("al") byte
    )
}
