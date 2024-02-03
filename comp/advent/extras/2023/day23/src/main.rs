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
type PolishedGraph<'a> = [&'a [(usize, i16)]; 64];

// !!! WARNING: BAD CODE !!!
fn polish_graph<'a>(input: &Graph, scratch: &'a mut [[(usize, i16); 64]; 64]) -> PolishedGraph<'a> {
    static EMPTY_SLICE: [(usize, i16); 0] = [];
    let mut polished: PolishedGraph<'a> = [&EMPTY_SLICE[..]; 64];
    let mut lens: Vec<usize> = Vec::new();

    for (i, xs) in input.iter().enumerate() {
        let edges: Vec<(usize, i16)> = xs
            .iter()
            .take_while(|x| x.is_some())
            .map(|x| x.unwrap())
            .collect();
        for (j, edge) in edges.iter().enumerate() {
            scratch[i][j] = *edge;
        }
        lens.push(edges.len());
    }

    for (i, len) in lens.iter().enumerate() {
        polished[i] = &scratch[i][..*len];
    }

    polished
}
/// !!! WARNING: BAD CODE !!!

fn main() -> EmptyResult {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input)?;

    let start = Instant::now();
    let grid = parse(&input);
    let (p1_graph, p1_start, p1_end) = collapse(&grid, true);
    let (p2_graph, p2_start, p2_end) = collapse(&grid, false);
    println!(
        "graphs:\t{:.3} ms",
        Instant::now().duration_since(start).as_micros() as f64 / 1000.0
    );

    let mut p1_scratch = [[(0, 0); 64]; 64];
    let mut p2_scratch = [[(0, 0); 64]; 64];
    let p1_graph = polish_graph(&p1_graph, &mut p1_scratch);
    let p2_graph = polish_graph(&p2_graph, &mut p2_scratch);

    let mut q = Vec::with_capacity(128);

    let start = Instant::now();
    let max_dist = dfs(&p1_graph, p1_end, p1_start, &mut q);
    println!(
        "p1:\t{:.3} ms\t({})",
        Instant::now().duration_since(start).as_micros() as f64 / 1000.0,
        max_dist
    );
    q.clear();

    let start = Instant::now();
    let max_dist = dfs(&p2_graph, p2_end, p2_start, &mut q);
    println!(
        "p2:\t{:.3} ms\t({})",
        Instant::now().duration_since(start).as_micros() as f64 / 1000.0,
        max_dist
    );

    let mut times: Vec<u128> = Vec::new();
    for _ in 0..100 {
        q.clear();
        let start = Instant::now();
        dfs(&p2_graph, p2_end, p2_start, &mut q);
        times.push(Instant::now().duration_since(start).as_nanos());
    }

    println!(
        "\np2 * 100:\nmax:\t{:.3} ms\nmin:\t{:.3} ms\navg:\t{:.3} ms",
        *times.iter().max().unwrap() as f64 / 1000000.0,
        *times.iter().min().unwrap() as f64 / 1000000.0,
        times.iter().map(|x| *x as f64).sum::<f64>() / (1000000.0 * 100.0),
    );

    assert!(q.capacity() <= 128); // never reallocated
    drop(q);

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
        data.get_mut(&(r, c)).unwrap().remove(&(r, c));
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

fn dfs(input: &PolishedGraph, goal: usize, start: usize, q: &mut Vec<(usize, u64, i16)>) -> i16 {
    let mut max = 0;
    q.push((start, 1u64 << start, 0));

    while let Some((current, visited, dist)) = q.pop() {
        input[current].iter().for_each(|(next, next_dist)| {
            if *next == goal {
                max = i16::max(max, dist + next_dist);
            } else {
                let next_mask = 1u64 << next;
                if (visited & next_mask) == 0 {
                    q.push((*next, visited | next_mask, dist + next_dist));
                }
            }
        })
    }

    max
}
