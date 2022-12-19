use std::io::{self, Read};

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
    // part 1
    let state = State {
        ore: 0,
        clay: 0,
        obi: 0,
        ore_robots: 1,
        clay_robots: 0,
        obi_robots: 0,
        geode_robots: 0,
        geodes: 0,
        ticks: 24,
    };
    let sum: usize = blueprints
        .iter()
        .enumerate()
        .map(|(i, b)| State::solve(b, state) as usize * (i + 1))
        .sum();
    println!("{}", sum);
    let state = State {
        ore: 0,
        clay: 0,
        obi: 0,
        ore_robots: 1,
        clay_robots: 0,
        obi_robots: 0,
        geode_robots: 0,
        geodes: 0,
        ticks: 32,
    };
    let sum = State::solve(&blueprints[0], state)
        * State::solve(&blueprints[1], state)
        * State::solve(&blueprints[2], state);
    println!("{}", sum);

    Ok(())
}

#[derive(Clone, Copy, Debug, Default)]
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

#[derive(Copy, Clone, Debug)]
enum Robot {
    Ore,
    Clay,
    Obi,
    Geode,
}

fn max(a: u16, b: u16) -> u16 {
    if a > b {
        a
    } else {
        b
    }
}

type Costs<'a> = &'a [(Robot, &'a Cost); 4];

impl State {
    fn solve(blueprint: &Blueprint, state: State) -> u16 {
        let costs = [
            (Robot::Ore, &blueprint.ore),
            (Robot::Clay, &blueprint.clay),
            (Robot::Obi, &blueprint.obi),
            (Robot::Geode, &blueprint.geode),
        ];
        state.best_substate(&costs)
    }

    fn best_substate(mut self, blueprint: Costs) -> u16 {
        let mut m = 0;
        let mut ore = false;
        let mut clay = false;
        let mut obi = false;
        while self.ticks > 0 {
            // check for build robots
            if ore && clay && obi {
                break;
            }
            // i dont think this is totally correct but it did work
            if self.can_build(blueprint[3].1) {
                m = max(m, self.build(blueprint[3]).best_substate(blueprint));
                break
            }
            if !ore && self.can_build(blueprint[0].1) {
                ore = true;
                m = max(m, self.build(blueprint[0]).best_substate(blueprint));
            }
            if !clay && self.can_build(blueprint[1].1) {
                clay = true;
                m = max(m, self.build(blueprint[1]).best_substate(blueprint));
            }
            if !obi && self.can_build(blueprint[2].1) {
                obi = true;
                m = max(m, self.build(blueprint[2]).best_substate(blueprint));
            }
            self.gen_resources();
            self.ticks -= 1;
        }
        m = max(m, self.geodes);
        m
    }

    #[inline]
    fn can_build(&self, cost: &Cost) -> bool {
        self.ore >= cost.ore && self.clay >= cost.clay && self.obi >= cost.obi
    }

    #[inline]
    fn gen_resources(&mut self) {
        self.ore += self.ore_robots;
        self.clay += self.clay_robots;
        self.obi += self.obi_robots;
        self.geodes += self.geode_robots;
    }

    #[inline]
    fn build(&self, robot: (Robot, &Cost)) -> Self {
        let mut new = *self;
        new.ore -= robot.1.ore;
        new.clay -= robot.1.clay;
        new.obi -= robot.1.obi;
        new.ticks -= 1;
        new.gen_resources();
        match robot.0 {
            Robot::Ore => new.ore_robots += 1,
            Robot::Clay => new.clay_robots += 1,
            Robot::Obi => new.obi_robots += 1,
            Robot::Geode => new.geode_robots += 1,
        };
        new
    }
}
