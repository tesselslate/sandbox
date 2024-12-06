#![allow(unused)]

use std::time::{Duration, Instant};

const LEN: usize = 130;
const SZ: usize = LEN * LEN;
const BITMAP_U64_COUNT: usize = SZ.div_ceil(64);

const DIRS: [(isize, isize); 4] = [(-1, 0), (0, 1), (1, 0), (0, -1)];

struct Grid([bool; SZ]);

impl Grid {
    #[inline(always)]
    pub fn get(&self, pos: (isize, isize)) -> bool {
        self.0[pos.0 as usize * LEN + pos.1 as usize]
    }

    #[inline(always)]
    pub fn set(&mut self, pos: (isize, isize), state: bool) {
        self.0[pos.0 as usize * LEN + pos.1 as usize] = state;
    }
}

impl Default for Grid {
    fn default() -> Self {
        Grid([false; SZ])
    }
}

#[derive(Copy, Clone)]
struct Visited([u64; BITMAP_U64_COUNT * 4]);

impl Visited {
    #[inline]
    pub fn contains(&self, dir: usize, pos: (isize, isize)) -> bool {
        let pos = (pos.0 * LEN as isize + pos.1) as usize * 4 + dir;
        let idx = pos / 64;
        let bit = pos % 64;

        return ((self.0[idx] >> bit) & 1) == 1;
    }

    #[inline]
    pub fn mark(&mut self, dir: usize, pos: (isize, isize)) {
        let pos = (pos.0 * LEN as isize + pos.1) as usize * 4 + dir;
        let idx = pos / 64;
        let bit = pos % 64;

        self.0[idx] |= 1 << bit;
    }
}

impl Default for Visited {
    fn default() -> Self {
        Self([0; BITMAP_U64_COUNT * 4])
    }
}

fn parse(input: &str) -> ((isize, isize), Grid) {
    let mut grid = Grid::default();
    let mut start_pos = None;

    let lines = input.lines();
    lines.enumerate().for_each(|(i, line)| {
        line.chars().enumerate().for_each(|(j, char)| {
            if char == '#' {
                grid.set((i as isize, j as isize), true);
            }

            if char == '^' {
                start_pos = Some((i as isize, j as isize));
            }
        });
    });

    (start_pos.expect("no start pos"), grid)
}

fn navigate(grid: &Grid, mut pos: (isize, isize), mut dir: usize, visited: &mut Visited) -> bool {
    loop {
        if visited.contains(dir, pos) {
            return true;
        }
        visited.mark(dir, pos);

        let new = (pos.0 + DIRS[dir].0, pos.1 + DIRS[dir].1);
        if new.0 < 0 || new.1 < 0 || new.0 >= LEN as isize || new.1 >= LEN as isize {
            return false;
        }

        if grid.get(new) {
            dir = (dir + 1) % 4;
        } else {
            pos = new;
        }
    }
}

fn find_obstructions(grid: &mut Grid, start: (isize, isize)) -> u32 {
    let mut visited = Visited::default();
    let mut visited_any = [0u64; BITMAP_U64_COUNT];
    let mut obstructions = [0u64; BITMAP_U64_COUNT];

    let mut pos = start;
    let mut dir = 0;

    loop {
        if visited.contains(dir, pos) {
            panic!("loop in find_obstructions");
        }
        visited.mark(dir, pos);

        let x = (pos.0 * LEN as isize + pos.1) as usize;
        let idx = x / 64;
        let bit = x % 64;
        visited_any[idx] |= 1 << bit;

        let new = (pos.0 + DIRS[dir].0, pos.1 + DIRS[dir].1);
        if new.0 < 0 || new.1 < 0 || new.0 >= LEN as isize || new.1 >= LEN as isize {
            return obstructions.iter().map(|u64| u64.count_ones()).sum();
        }

        if grid.get(new) {
            dir = (dir + 1) % 4;
        } else {
            let x = (new.0 * LEN as isize + new.1) as usize;
            let idx = x / 64;
            let bit = x % 64;

            if ((visited_any[idx] >> bit) & 1) == 0 {
                grid.set(new, true);
                if navigate(grid, pos, (dir + 1) % 4, &mut visited.clone()) {
                    obstructions[idx] |= 1 << bit;
                }
                grid.set(new, false);
            }

            pos = new;
        }
    }
}

pub fn run(input: &str, runs: usize) -> Vec<Duration> {
    let (start_pos, mut grid) = parse(&input);

    let mut durations = Vec::new();
    for _ in 0..runs {
        let start = Instant::now();
        find_obstructions(&mut grid, start_pos);
        durations.push(Instant::now().duration_since(start));
    }
    durations
}
