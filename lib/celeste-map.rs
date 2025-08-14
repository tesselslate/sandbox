use std::{
    borrow::Cow,
    collections::HashMap,
    fmt::Debug,
    io::{Cursor, Read},
};

use byteorder::{ReadBytesExt, LE};

#[derive(Debug)]
pub struct Map<'a> {
    name: String,
    root: Element<'a>,
}

#[derive(Debug)]
pub struct Element<'a> {
    name: &'a str,
    attributes: HashMap<&'a str, Attribute<'a>>,
    children: Vec<Element<'a>>,
}

#[derive(Debug)]
pub enum Attribute<'a> {
    Bool(bool),
    Int(i32),
    Float(f32),
    String(Cow<'a, str>),
}

/// Provides various methods for reading data written by C#'s BinaryWriter
/// class.
trait ReadBinary: Read {
    /// Reads a variable-length unsigned integer from the binary stream, where
    /// the lowest 7 bits of each byte contain the bits of the integer.
    fn read_var_uint(&mut self) -> anyhow::Result<usize> {
        let mut value = 0;

        loop {
            let byte = self.read_u8()?;
            value = (value << 7) | (byte & 0x7F) as usize;

            if (byte & 0x80) == 0 {
                break;
            }
        }

        Ok(value)
    }

    /// Reads a length-prefixed string from the binary stream.
    fn read_string(&mut self) -> anyhow::Result<String> {
        let mut bytes = vec![0u8; self.read_var_uint()?];
        self.read_exact(bytes.as_mut_slice())?;

        Ok(String::from_utf8(bytes)?)
    }
}

impl<T: Read> ReadBinary for T {}

/// Provides various methods for reading components of a Celeste map file.
trait ReadElement<'a>: ReadBinary {
    /// Reads a string from the map file's lookup table using the next ID in the
    /// binary stream.
    fn read_lut_string(&mut self, lut: &'a [String]) -> anyhow::Result<&'a str> {
        let id: usize = self.read_i16::<LE>()?.try_into()?;

        match lut.get(id) {
            Some(str) => Ok(str.as_str()),
            None => Err(anyhow::anyhow!("invalid string ID {}", id)),
        }
    }

    /// Reads a run length encoded string from the map file.
    fn read_rle_string(&mut self) -> anyhow::Result<String> {
        let len: usize = self.read_i16::<LE>()?.try_into()?;
        let mut bytes = vec![0u8; len];
        self.read_exact(bytes.as_mut_slice())?;

        let mut value = String::with_capacity(1024);
        bytes.chunks(2).try_for_each(|chunk| {
            if chunk.len() != 2 {
                return Err(anyhow::anyhow!(
                    "run-length-encoded string has partial chunk"
                ));
            }

            let len = chunk[0] as usize;
            let byte = chunk[1];

            value.extend(std::iter::repeat_n(byte as char, len));

            Ok(())
        })?;

        Ok(value)
    }

    /// Reads a full element from the map file.
    fn read_element(&mut self, lut: &'a [String]) -> anyhow::Result<Element<'a>> {
        let name = self.read_lut_string(lut)?;

        let attr_count = self.read_u8()? as usize;
        let attributes = if attr_count > 0 {
            let mut attributes = HashMap::with_capacity(attr_count);

            for _ in 0..attr_count {
                attributes.insert(
                    self.read_lut_string(lut)?,
                    match self.read_u8()? {
                        0 => Attribute::Bool(self.read_u8()? != 0),
                        1 => Attribute::Int(self.read_i8()? as i32),
                        2 => Attribute::Int(self.read_i16::<LE>()? as i32),
                        3 => Attribute::Int(self.read_i32::<LE>()?),
                        4 => Attribute::Float(self.read_f32::<LE>()?),
                        5 => Attribute::String(Cow::Borrowed(self.read_lut_string(lut)?)),
                        6 => Attribute::String(Cow::Owned(self.read_string()?)),
                        7 => Attribute::String(Cow::Owned(self.read_rle_string()?)),
                        typ => return Err(anyhow::anyhow!("invalid attribute type {}", typ)),
                    },
                );
            }

            attributes
        } else {
            HashMap::new()
        };

        let child_count: usize = self.read_i16::<LE>()?.try_into()?;
        let mut children = Vec::with_capacity(child_count);
        for _ in 0..child_count {
            children.push(self.read_element(lut)?);
        }

        Ok(Element {
            name,
            attributes,
            children,
        })
    }
}

impl<T: ReadBinary> ReadElement<'_> for T {}

impl TryFrom<&[u8]> for Map<'_> {
    type Error = anyhow::Error;

    fn try_from(value: &[u8]) -> Result<Self, Self::Error> {
        let mut r = Cursor::new(value);

        if r.read_string()? != "CELESTE MAP" {
            return Err(anyhow::anyhow!("invalid header string"));
        }

        let map_name = r.read_string()?;

        let lut_size: usize = r.read_i16::<LE>()?.try_into()?;
        let mut lut = Vec::with_capacity(lut_size);
        for _ in 0..lut_size {
            lut.push(r.read_string()?);
        }

        // TODO: Avoid leaking the LUT. This is annoying since the `root` field
        // of Map is self-referential, since it references strings from the
        // `lut` field.
        let lut: &'static Vec<String> = Box::leak(Box::new(lut));

        Ok(Map {
            name: map_name,
            root: r.read_element(lut)?,
        })
    }
}
