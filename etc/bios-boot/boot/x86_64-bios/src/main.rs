#![no_main]
#![no_std]

/// Provides facilities for interacting with
/// input/output ports.
pub mod port;

/// Implements a basic 16550 UART driver.
/// Refer to [the OSDev wiki](https://wiki.osdev.org/Serial_Ports) 
/// for more information.
pub mod uart;

use core::arch::asm;
use core::panic::PanicInfo;

use uart::Uart;

#[panic_handler]
fn panic(_: &PanicInfo) -> ! {
    loop {
        unsafe { asm!("hlt"); }
    }
}

static BOOT_MSG: &[u8] = b"Rust: Entered stage 3!";

#[no_mangle]
pub unsafe extern "C" fn _start() -> ! {
    let ptr = 0xb8000 as *mut u8;
    
    // clear screen
    for i in 0 .. 80 * 25 {
        ptr.offset(i as isize * 2).write_volatile(0);
    }

    // disable VGA text mode cursor
    port::write(0x3d4, 0x0a);
    port::write(0x3d5, 0x20);

    // setup UART, write boot message
    let uart = Uart::new(0x3f8).unwrap();
    uart.write_slice(BOOT_MSG);

    loop {
        asm!("hlt");
    }
}
