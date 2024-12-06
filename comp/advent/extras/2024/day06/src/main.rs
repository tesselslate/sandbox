use std::io::{self, Read};

mod basic;
mod basic2;

type EmptyResult = Result<(), Box<dyn std::error::Error>>;

fn main() -> EmptyResult {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input)?;

    basic::run(&input)?;
    basic2::run(&input)?;
    Ok(())
}
