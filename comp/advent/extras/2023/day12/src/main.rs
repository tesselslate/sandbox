use hashbrown::HashMap;
use std::io::{self, Read};
use std::time::Instant;

type EmptyResult = Result<(), Box<dyn std::error::Error>>;

#[derive(PartialEq, Eq, Copy, Clone, Debug)]
enum Spring {
    Operational,
    Damaged,
    Unknown,
}

#[derive(Clone)]
struct Entry {
    springs: Vec<Spring>,
    damaged: Vec<u8>,
}

fn main() -> EmptyResult {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input)?;

    let entries: Vec<Entry> = parse(&input);

    let now = Instant::now();
    part1(&entries)?;
    part2(&entries)?;
    let duration = Instant::now().duration_since(now);
    println!("{} us", duration.as_micros());

    Ok(())
}

fn parse(input: &String) -> Vec<Entry> {
    let mut out = Vec::new();

    for line in input.lines() {
        let (a, b) = line.split_once(" ").unwrap();

        let springs = a
            .chars()
            .map(|ch| match ch {
                '#' => Spring::Damaged,
                '.' => Spring::Operational,
                '?' => Spring::Unknown,
                _ => unreachable!(),
            })
            .collect::<Vec<Spring>>();
        let damaged = b
            .split(',')
            .map(|num| num.parse().unwrap())
            .collect::<Vec<u8>>();
        out.push(Entry { springs, damaged });
    }

    out
}

fn part1(input: &Vec<Entry>) -> EmptyResult {
    let ans: usize = input
        .iter()
        .map(|entry| {
            let mut memo = HashMap::new();
            let v = combinations(
                &mut memo,
                entry,
                State {
                    spring_idx: 0,
                    damage_idx: 0,
                    prev_damaged: 0,
                },
            );
            v
        })
        .sum();
    println!("{}", ans);

    Ok(())
}

fn part2(input: &Vec<Entry>) -> EmptyResult {
    let input = preprocess_p2(input);

    let mut memo = HashMap::new();
    let ans: usize = input
        .iter()
        .map(|entry| {
            let v = combinations(
                &mut memo,
                entry,
                State {
                    spring_idx: 0,
                    damage_idx: 0,
                    prev_damaged: 0,
                },
            );
            memo.clear();
            v
        })
        .sum();
    println!("{}", ans);

    Ok(())
}

#[derive(Hash, PartialEq, Eq, Copy, Clone)]
struct State {
    spring_idx: u8,
    damage_idx: u8,
    prev_damaged: u8,
}

fn combinations(memo: &mut HashMap<State, usize>, input: &Entry, mut state: State) -> usize {
    if let Some(v) = memo.get(&state) {
        return *v;
    }

    let state_copy = state;

    while state.spring_idx < input.springs.len() as u8
        && input.springs[state.spring_idx as usize] != Spring::Unknown
    {
        match input.springs[state.spring_idx as usize] {
            Spring::Operational => {
                if state.prev_damaged > 0 {
                    if state.damage_idx == input.damaged.len() as u8
                        || input.damaged[state.damage_idx as usize] != state.prev_damaged
                    {
                        return 0;
                    }
                    state.prev_damaged = 0;
                    state.damage_idx += 1;
                }
            }
            Spring::Damaged => {
                state.prev_damaged += 1;
            }
            Spring::Unknown => unreachable!(),
        }
        state.spring_idx += 1;
    }
    if state.spring_idx == input.springs.len() as u8 {
        if state.prev_damaged > 0 {
            if state.damage_idx == input.damaged.len() as u8
                || input.damaged[state.damage_idx as usize] != state.prev_damaged
            {
                return 0;
            }
        }

        return if state.damage_idx == input.damaged.len() as u8 {
            1
        } else {
            0
        };
    }

    let mut sum: usize = 0;

    // damaged
    let new_state = State {
        spring_idx: state.spring_idx + 1,
        damage_idx: state.damage_idx,
        prev_damaged: state.prev_damaged + 1,
    };
    sum += combinations(memo, input, new_state);

    // operational
    let new_state = if state.prev_damaged > 0 {
        if state.damage_idx == input.damaged.len() as u8
            || input.damaged[state.damage_idx as usize] != state.prev_damaged
        {
            None
        } else {
            Some(State {
                spring_idx: state.spring_idx + 1,
                damage_idx: state.damage_idx + 1,
                prev_damaged: 0,
            })
        }
    } else {
        Some(State {
            spring_idx: state.spring_idx + 1,
            damage_idx: state.damage_idx,
            prev_damaged: 0,
        })
    };
    if let Some(new_state) = new_state {
        sum += combinations(memo, input, new_state);
    }

    memo.insert(state_copy, sum);
    sum
}

fn preprocess_p2(input: &Vec<Entry>) -> Vec<Entry> {
    let mut input = input.to_vec();
    for entry in input.iter_mut() {
        entry.springs.push(Spring::Unknown);
        entry.springs = entry
            .springs
            .iter()
            .cycle()
            .take(entry.springs.len() * 5)
            .map(|x| *x)
            .collect();
        entry.damaged = entry
            .damaged
            .iter()
            .cycle()
            .take(entry.damaged.len() * 5)
            .map(|x| *x)
            .collect();
    }

    input
}

fn _solve_naive(input: &Vec<Entry>) -> usize {
    input
        .iter()
        .map(|entry| {
            let indices: Vec<usize> = entry
                .springs
                .iter()
                .enumerate()
                .filter(|(_, spring)| **spring == Spring::Unknown)
                .map(|(i, _)| i)
                .collect();
            let mut springs = entry.springs.clone();
            let mut counts: Vec<u8> = Vec::with_capacity(entry.damaged.len());
            (0..1 << indices.len())
                .filter(|unknown_key| {
                    for i in 0..indices.len() {
                        let spring = if ((unknown_key >> i) & 1) == 1 {
                            Spring::Damaged
                        } else {
                            Spring::Operational
                        };
                        springs[indices[i]] = spring;
                    }

                    counts.clear();
                    let mut count = 0u8;
                    for spring in &springs {
                        match *spring {
                            Spring::Damaged => count += 1,
                            Spring::Operational => {
                                if count > 0 {
                                    counts.push(count);
                                }
                                count = 0;
                            }
                            Spring::Unknown => unreachable!(),
                        }
                    }
                    if count > 0 {
                        counts.push(count);
                    }

                    counts == entry.damaged
                })
                .count()
        })
        .sum()
}
