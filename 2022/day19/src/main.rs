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
    let sum: usize = blueprints
        .iter()
        .enumerate()
        .map(|(i, b)| State::solve(b) as usize * (i + 1))
        .sum();
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
    None,
    Ore,
    Clay,
    Obi,
    Geode,
}

impl State {
    fn solve(blueprint: &Blueprint) -> u16 {
        let state = Self {
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
        state.best_substate(blueprint)
    }

    fn best_substate(&self, blueprint: &Blueprint) -> u16 {
        let states = self.generate_substates(blueprint);
        let mut max = 0;
        for state in states {
            if state.ticks == 0 {
                if state.geodes > max {
                    max = state.geodes;
                }
                continue;
            }
            let best = state.best_substate(blueprint);
            if best > max {
                max = best;
            }
        }
        max
    }

    fn generate_substates(&self, blueprint: &Blueprint) -> [Self; 5] {
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

        let mut res: [Self; 5] = [State::default(); 5];
        for (idx, (robot, cost)) in costs.iter().enumerate() {
            res[idx] = self.generate_substate(cost, *robot);
        }
        res
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
