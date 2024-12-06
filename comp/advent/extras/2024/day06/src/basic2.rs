use std::time::Instant;

type EmptyResult = Result<(), Box<dyn std::error::Error>>;

const LEN: usize = 130;
const SZ: usize = LEN * LEN;
const BITMAP_U64_COUNT: usize = SZ.div_ceil(64);

const DIRS: [(isize, isize); 4] = [(-1, 0), (0, 1), (1, 0), (0, -1)];

type Grid = [[bool; 130]; 130];

#[derive(Copy, Clone)]
struct Visited([[u64; BITMAP_U64_COUNT]; 4]);

impl Visited {
    #[inline]
    pub fn contains(&self, dir: usize, pos: (isize, isize)) -> bool {
        let pos = (pos.0 * LEN as isize + pos.1) as usize;
        let idx = pos / 64;
        let bit = pos % 64;

        return ((self.0[dir][idx] >> bit) & 1) == 1;
    }

    #[inline]
    pub fn mark(&mut self, dir: usize, pos: (isize, isize)) {
        let pos = (pos.0 * LEN as isize + pos.1) as usize;
        let idx = pos / 64;
        let bit = pos % 64;

        self.0[dir][idx] |= 1 << bit;
    }

    pub fn total(&self) -> u32 {
        self.sum_maps().iter().map(|u64| u64.count_ones()).sum()
    }

    fn sum_maps(&self) -> [u64; BITMAP_U64_COUNT] {
        let mut all = [0u64; BITMAP_U64_COUNT];

        self.0
            .iter()
            .for_each(|arr| arr.iter().enumerate().for_each(|(i, u64)| all[i] |= u64));

        all
    }
}

impl Default for Visited {
    fn default() -> Self {
        Self([[0; BITMAP_U64_COUNT]; 4])
    }
}

fn parse(input: &str) -> ((isize, isize), Grid) {
    let mut grid = [[false; 130]; 130];
    let mut start_pos = None;

    let lines = input.lines();
    lines.enumerate().for_each(|(i, line)| {
        line.chars().enumerate().for_each(|(j, char)| {
            grid[i][j] = char == '#';

            if char == '^' {
                start_pos = Some((i as isize, j as isize));
            }
        });
    });

    (start_pos.expect("no start pos"), grid)
}

fn navigate(grid: &Grid, start: (isize, isize), visited: &mut Visited) -> bool {
    let mut pos = start;
    let mut dir = 0;

    loop {
        if visited.contains(dir, pos) {
            return true;
        }
        visited.mark(dir, pos);

        let new = (pos.0 + DIRS[dir].0, pos.1 + DIRS[dir].1);
        if new.0 < 0 || new.1 < 0 || new.0 >= LEN as isize || new.1 >= LEN as isize {
            return false;
        }

        if grid[new.0 as usize][new.1 as usize] {
            dir = (dir + 1) % 4;
        } else {
            pos = new;
        }
    }
}

fn navigate2(
    grid: &Grid,
    obstruct: (isize, isize),
    mut pos: (isize, isize),
    mut dir: usize,
    visited: &mut Visited,
) -> bool {
    loop {
        if visited.contains(dir, pos) {
            return true;
        }
        visited.mark(dir, pos);

        let new = (pos.0 + DIRS[dir].0, pos.1 + DIRS[dir].1);
        if new.0 < 0 || new.1 < 0 || new.0 >= LEN as isize || new.1 >= LEN as isize {
            return false;
        }

        if grid[new.0 as usize][new.1 as usize] || obstruct == new {
            dir = (dir + 1) % 4;
        } else {
            pos = new;
        }
    }
}

fn find_obstructions(grid: &Grid, start: (isize, isize)) -> u32 {
    let mut visited = Visited::default();
    let mut obstructions = [0u64; BITMAP_U64_COUNT];

    let mut pos = start;
    let mut dir = 0;

    loop {
        if visited.contains(dir, pos) {
            panic!("loop in find_obstructions");
        }
        visited.mark(dir, pos);

        let new = (pos.0 + DIRS[dir].0, pos.1 + DIRS[dir].1);
        if new.0 < 0 || new.1 < 0 || new.0 >= LEN as isize || new.1 >= LEN as isize {
            return obstructions.iter().map(|u64| u64.count_ones()).sum();
        }

        if grid[new.0 as usize][new.1 as usize] {
            dir = (dir + 1) % 4;
        } else {
            if (!visited.contains(0, new)
                && !visited.contains(1, new)
                && !visited.contains(2, new)
                && !visited.contains(3, new))
                && navigate2(grid, new, pos, (dir + 1) % 4, &mut visited.clone())
            {
                let x = (new.0 * LEN as isize + new.1) as usize;
                let idx = x / 64;
                let bit = x % 64;
                obstructions[idx] |= 1 << bit;
            }

            pos = new;
        }
    }
}

pub fn run(input: &str) -> EmptyResult {
    let start = Instant::now();
    let (start_pos, grid) = parse(&input);
    println!(
        "parse:\t{:.3} ms",
        Instant::now().duration_since(start).as_micros() as f64 / 1000.0
    );

    let mut visited = Visited::default();

    let start = Instant::now();
    navigate(&grid, start_pos, &mut visited);
    let total = visited.total();
    println!(
        "part 1:\t{:.3} ms ({})",
        Instant::now().duration_since(start).as_micros() as f64 / 1000.0,
        total
    );

    let start = Instant::now();
    let total = find_obstructions(&grid, start_pos);
    println!(
        "part 2:\t{:.3}ms ({})",
        Instant::now().duration_since(start).as_micros() as f64 / 1000.0,
        total
    );

    Ok(())
}
