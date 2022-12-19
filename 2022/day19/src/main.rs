use std::{
    cmp::Ordering,
    collections::{BinaryHeap, HashMap},
    hash::{Hash, Hasher},
    io::{self, Read},
};

type EmptyResult = Result<(), Box<dyn std::error::Error>>;

#[derive(Debug)]
struct Cost {
    ore: u16,
    clay: u16,
    obi: u16,
}

#[derive(Debug)]
struct Blueprint {
    ore: Cost,
    clay: Cost,
    obi: Cost,
    geode: Cost,
}

fn parse(input: &String) -> Vec<Blueprint> {
    input.lines().map(|l| {
        let (_, ore_ore, clay_ore, obi_ore, obi_clay, geode_ore, geode_obi) = sscanf::sscanf!(l, "Blueprint {u16}: Each ore robot costs {u16} ore. Each clay robot costs {u16} ore. Each obsidian robot costs {u16} ore and {u16} clay. Each geode robot costs {u16} ore and {u16} obsidian.").unwrap();
        Blueprint {
            ore: Cost {ore: ore_ore, clay: 0, obi: 0},
            clay: Cost {ore: clay_ore, clay: 0, obi: 0},
            obi: Cost {ore: obi_ore, clay: obi_clay, obi: 0},
            geode: Cost {ore: geode_ore, clay: 0, obi: geode_obi}
        }
    }).collect()
}

pub fn main() -> EmptyResult {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input)?;
    let blueprints = parse(&input);
    let sum: usize = blueprints
        .iter()
        .enumerate()
        .map(|(i, b)| Solver::solve(Solver::new(), b) as usize * (i + 1))
        .sum();
    println!("{}", sum);
    Ok(())
}

#[derive(Clone, Copy, Debug, Default, Eq)]
struct State {
    ore: u16,
    clay: u16,
    obi: u16,

    ore_robots: u16,
    clay_robots: u16,
    obi_robots: u16,
    geode_robots: u16,

    geodes: u16,
    ticks: u8,
}

#[derive(Debug)]
enum Robot {
    None,
    Ore,
    Clay,
    Obi,
    Geode,
}

impl State {
    fn generate_substates(&self, blueprint: &Blueprint, res: &mut Vec<Self>) {
        let costs = [
            (
                Robot::None,
                &Cost {
                    ore: 0,
                    clay: 0,
                    obi: 0,
                },
            ),
            (Robot::Ore, &blueprint.ore),
            (Robot::Clay, &blueprint.clay),
            (Robot::Obi, &blueprint.obi),
            (Robot::Geode, &blueprint.geode),
        ];

        for (robot, cost) in costs {
            res.push(self.generate_substate(cost, robot));
        }
    }

    #[inline]
    fn generate_substate(&self, cost: &Cost, robot: Robot) -> Self {
        // can this robot get built
        let mut new = *self;
        new.ticks -= 1;
        let can_build = self.ore >= cost.ore && self.clay >= cost.clay && self.obi >= cost.obi;
        new.ore += new.ore_robots;
        new.clay += new.clay_robots;
        new.obi += new.obi_robots;
        new.geodes += new.geode_robots;
        if can_build {
            match robot {
                Robot::Ore => new.ore_robots += 1,
                Robot::Clay => new.clay_robots += 1,
                Robot::Obi => new.obi_robots += 1,
                Robot::Geode => new.geode_robots += 1,
                _ => (),
            };
        }
        new
    }
}

impl Hash for State {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.ore.hash(state);
        self.clay.hash(state);
        self.obi.hash(state);
        self.ore_robots.hash(state);
        self.clay_robots.hash(state);
        self.obi_robots.hash(state);
        self.geode_robots.hash(state);
    }
}

impl PartialEq for State {
    fn eq(&self, other: &Self) -> bool {
        self.ore == other.ore
            && self.clay == other.clay
            && self.obi == other.obi
            && self.ore_robots == other.ore_robots
            && self.obi_robots == other.obi_robots
            && self.clay_robots == other.clay_robots
            && self.geode_robots == other.geode_robots
    }
}

// TODO: optimize ordering?
impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        self
            .geodes
            .cmp(&other.geodes)
            .then(self.ticks.cmp(&other.ticks))
            .then(self.geode_robots.cmp(&other.geode_robots))
            .then(self.obi_robots.cmp(&other.obi_robots))
            .then(self.clay_robots.cmp(&other.clay_robots))
            .then(self.ore_robots.cmp(&other.ore_robots))
            .then(self.obi.cmp(&other.obi))
            .then(self.clay.cmp(&other.obi))
            .then(self.ore.cmp(&other.ore))
    }
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

struct Solver {
    states: HashMap<State, u16>,
    queue: BinaryHeap<State>,
}

impl Solver {
    fn new() -> Self {
        Self {
            states: HashMap::new(),
            queue: BinaryHeap::new(),
        }
    }

    fn solve(mut self, blueprint: &Blueprint) -> u16 {
        let mut s = State::default();
        let mut v = Vec::new();
        s.ore_robots = 1;
        s.ticks = 24;
        self.queue.push(s);

        while let Some(state) = self.queue.pop() {
            if state.ticks == 0 {
                println!("{}", state.geodes);
                return state.geodes
            }

            if state.geodes > 0 {
                println!("{:?} {}", state, self.states.len());
            }

            if let Some(score) = self.states.get_mut(&state) {
                if *score < state.geodes {
                    continue;
                } else {
                    *score = state.geodes;
                }
            }

            v.clear();
            state.generate_substates(blueprint, &mut v);
            for state in &v {
                if let Some(score) = self.states.get_mut(&state) {
                    if *score < state.geodes {
                        continue;
                    } else {
                        *score = state.geodes;
                        self.queue.push(*state);
                    }
                } else {
                    self.queue.push(*state);
                    self.states.insert(*state, state.geodes);
                }
            }
        }
        u16::MAX
    }
}
