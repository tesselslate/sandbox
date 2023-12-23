use rayon::prelude::*;
use std::collections::{HashMap, HashSet, VecDeque};
use std::io::{self, Read};
use std::time::Instant;

type EmptyResult = Result<(), Box<dyn std::error::Error>>;

#[derive(Copy, Clone, PartialEq, Eq)]
enum Tile {
    Wall,
    Empty,
    LeftSlope,
    RightSlope,
    DownSlope,
    UpSlope,
}

struct Grid {
    data: Vec<Tile>,
    width: usize,
    height: usize,
}

impl Grid {
    fn inbounds(&self, r: usize, c: usize) -> bool {
        return r < self.height && c < self.width;
    }

    fn tile(&self, r: usize, c: usize) -> Tile {
        return self.data[r * self.width + c];
    }
}

type Graph = [[Option<(usize, i16)>; 64]; 64];

fn main() -> EmptyResult {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input)?;

    let entries = parse(&input);

    let now = Instant::now();
    let x = part1(&entries);
    let duration = Instant::now().duration_since(now);
    println!("part 1: {} ({} micros)", x, duration.as_micros());

    let now = Instant::now();
    let x = part2(&entries);
    let duration = Instant::now().duration_since(now);
    println!("part 2: {} ({} micros)", x, duration.as_micros());

    Ok(())
}

fn parse(input: &String) -> Grid {
    let lines: Vec<&str> = input.lines().collect();
    let width = lines.first().unwrap().len().try_into().unwrap();
    let height = lines.len().try_into().unwrap();
    let mut data = Vec::with_capacity((width * height) as usize);
    for line in lines {
        for char in line.chars() {
            data.push(match char {
                '#' => Tile::Wall,
                '.' => Tile::Empty,
                '>' => Tile::RightSlope,
                '<' => Tile::LeftSlope,
                'v' => Tile::DownSlope,
                '^' => Tile::UpSlope,
                _ => unreachable!(),
            })
        }
    }

    assert!(data.len() == width * height);

    Grid {
        data,
        width,
        height,
    }
}

fn poi(sr: usize, sc: usize, input: &Grid, climbing: bool) -> HashMap<(usize, usize), i16> {
    let mut data: HashMap<(usize, usize), i16> = HashMap::new();
    let mut q: VecDeque<(usize, usize, i16)> = VecDeque::new();
    let mut visited: HashSet<(usize, usize)> = HashSet::new();

    q.push_back((sr, sc, 0));
    visited.insert((sr, sc));

    while let Some((r, c, d)) = q.pop_front() {
        let adjacent = [
            (Tile::DownSlope, r + 1, c),
            (Tile::UpSlope, r - 1, c),
            (Tile::RightSlope, r, c + 1),
            (Tile::LeftSlope, r, c - 1),
        ];

        let mut n = 0;
        let nq: Vec<(usize, usize, i16)> = adjacent
            .iter()
            .filter_map(|(ok, rr, cc)| {
                if !input.inbounds(*rr, *cc) {
                    data.insert((r, c), d);
                    return None;
                }

                let tile = input.tile(*rr, *cc);
                if tile == Tile::Wall {
                    return None;
                }
                n += 1;

                if visited.contains(&(*rr, *cc)) {
                    return None;
                }

                if !climbing || (tile == Tile::Empty || tile == *ok) {
                    Some((*rr, *cc, d + 1))
                } else {
                    None
                }
            })
            .collect();
        if n > 2 {
            data.insert((r, c), d);
        }
        if n <= 2 || (r, c) == (sr, sc) {
            q.extend(&nq);
            visited.extend(nq.iter().map(|(r, c, _)| (*r, *c)));
        }
    }

    data
}

fn collapse(input: &Grid, climbing: bool) -> (Graph, usize, usize) {
    let mut data: HashMap<(usize, usize), HashMap<(usize, usize), i16>> = HashMap::new();
    let mut q: VecDeque<(usize, usize)> = VecDeque::new();
    q.push_back((0, 1));

    while let Some((r, c)) = q.pop_front() {
        let points = poi(r, c, input, climbing);
        for k in points.keys() {
            if !data.contains_key(k) {
                data.insert(*k, HashMap::new());
                q.push_back(*k);
            }
        }
        data.insert((r, c), points);
    }

    assert!(data.len() <= 64);

    let keys: HashMap<(usize, usize), usize> =
        data.keys().enumerate().map(|(i, k)| (*k, i)).collect();
    let mut graph: Graph = [[None; 64]; 64];
    for (key, id) in &keys {
        for (i, (point, dist)) in data.get(&key).unwrap().iter().enumerate() {
            let point_id = &keys.get(&point).unwrap();
            graph[*id][i] = Some((**point_id, *dist));
        }
    }

    (
        graph,
        *keys.get(&(0, 1)).unwrap(),
        *keys.get(&(input.height - 1, input.width - 2)).unwrap(),
    )
}

fn dfs(input: &Graph, goal: usize, current: usize, dist: i16, visited: u64) -> i16 {
    input[current]
        .iter()
        .take_while(|x| x.is_some())
        .map(|x| {
            let (next, next_dist) = x.unwrap();
            if next == goal {
                return dist + next_dist;
            }

            let next_mask = 1u64 << next;
            if (visited & next_mask) == 0 {
                dfs(input, goal, next, dist + next_dist, visited | next_mask)
            } else {
                0
            }
        })
        .max()
        .unwrap()
}

fn bfs(input: &Graph, depth: usize, goal: usize, current: usize, dist: i16, visited: u64) -> i16 {
    input[current]
        .par_iter()
        .filter(|x| x.is_some())
        .map(|x| {
            let (next, next_dist) = x.unwrap();
            if next == goal {
                return dist + next_dist;
            }

            let next_mask = 1u64 << next;
            if (visited & next_mask) == 0 {
                if depth > 0 {
                    bfs(
                        input,
                        depth - 1,
                        goal,
                        next,
                        dist + next_dist,
                        visited | next_mask,
                    )
                } else {
                    dfs(input, goal, next, dist + next_dist, visited | next_mask)
                }
            } else {
                0
            }
        })
        .max()
        .unwrap()
}

fn part1(input: &Grid) -> i16 {
    let (graph, start, end) = collapse(input, true);
    let visited = 1u64 << start;
    dfs(&graph, end, start, 0, visited)
}

fn part2(input: &Grid) -> i16 {
    let (graph, start, end) = collapse(input, false);
    let visited = 1u64 << start;
    bfs(&graph, 12, end, start, 0, visited)
}
