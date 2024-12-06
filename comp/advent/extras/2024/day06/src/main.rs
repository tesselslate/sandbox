use std::{
    io::{self, Read},
    time::Duration,
};

mod solve;

type EmptyResult = Result<(), Box<dyn std::error::Error>>;

const RUNS: usize = 100;

fn main() -> EmptyResult {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input)?;

    for _ in 0..10 {
        let times = solve::run(&input, RUNS);

        println!(
            "min: {:.3} ms",
            times.iter().min().unwrap().as_micros() as f64 / 1000.0
        );
        println!(
            "max: {:.3} ms",
            times.iter().max().unwrap().as_micros() as f64 / 1000.0
        );
        println!(
            "avg: {:.3} ms",
            times.iter().sum::<Duration>().as_micros() as f64 / 1000.0 / RUNS as f64
        );
        println!("================");
    }

    Ok(())
}
