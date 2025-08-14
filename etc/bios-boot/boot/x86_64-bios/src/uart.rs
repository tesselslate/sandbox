use crate::port;

/// Contains basic functionality for driving
/// a 16550 UART over a serial port.
pub struct Uart {
    /// The base port which the UART is on.
    base_port: u16
}

// https://wiki.osdev.org/Serial_Ports#Example_Code
impl Uart {
    /// Creates a new Uart struct with the given
    /// port and initializes the physical UART.
    pub fn new(base: u16) -> Option<Self> {
        let uart = Self {
            base_port: base
        };

        unsafe {
            port::write(base + 1, 0x00);  // disable interrupts
            port::write(base + 3, 0x80);  // enable DLAB
            port::write(base,     0x03);  // set divisor to 3
            port::write(base + 1, 0x00);
            port::write(base + 3, 0x03);  // 8 bits, no parity, 1 stop bit
            port::write(base + 2, 0xc7);  // FIFO, clear, 14 byte threshold
            port::write(base + 4, 0x0b);  // IRQs, RTS/DSR
            port::write(base + 4, 0x1e);  // loopback and test
            port::write(base,     0xae);  // test serial chip

            // check to see that same byte was received
            if port::read(base) != 0xae {
                None
            } else {
                // UART is good, set back to normal mode
                port::write(base + 4, 0x0f);

                Some(uart)
            }
        }
    }

    /// Writes a byte to the UART.
    ///
    /// Will block in a busy loop as long as necessary
    /// to wait for the IO port to empty.
    pub fn write(&self, input: u8) {
        while !self.is_empty() {}
        unsafe { port::write(self.base_port, input); }
    }

    /// Writes a byte slice to the UART.
    ///
    /// Will block in a busy loop as long as necessary
    /// to wait for the IO port to empty.
    pub fn write_slice(&self, input: &[u8]) {
        for byte in input {
            self.write(*byte);
        }
    }

    /// Receives a byte from the UART.
    ///
    /// Will block in a busy loop as long as necessary
    /// to wait for a message.
    pub fn read(&self) -> u8 {
        while self.is_empty_recv() {}

        unsafe { port::read(self.base_port) }
    }

    /// Will return a byte from the UART if one has been
    /// received. Otherwise, None will be returned.
    pub fn try_read(&self) -> Option<u8> {
        if !self.is_empty_recv() {
            unsafe { Some(port::read(self.base_port)) }
        } else {
            None
        }
    }

    /// Determines whether or not the transmitter is empty.
    fn is_empty(&self) -> bool {
        unsafe { port::read(self.base_port + 5) & 0x20 != 0 }
    }

    /// Determines whether or not a byte has been received.
    fn is_empty_recv(&self) -> bool {
        unsafe { port::read(self.base_port + 5) & 0x01 == 0 }
    }
}
