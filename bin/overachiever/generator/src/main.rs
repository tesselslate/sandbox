use std::{fs::File, io::{BufReader, Read}, collections::HashSet};

use crunch::{Item, Rotation};
use image::{RgbaImage, ImageBuffer, GenericImage, DynamicImage};
use zip::ZipArchive;

// based off of:
// https://github.com/ChevyRay/crunch-rs/blob/master/examples/pack_images/src/main.rs

pub struct CrunchItem {
    pub image: RgbaImage,
    pub name: String
}

fn print_ok<T>(msg: T) where T: Into<String> + std::fmt::Display {
    println!("\x1b[1;32mok:\x1b[0m {}", msg);
}

fn print_err<T>(msg: T) -> ! where T: Into<String> + std::fmt::Display {
    println!("\x1b[1;31merr:\x1b[0m {}", msg);
    std::process::exit(1);
}

pub enum Sheet {
    Biome,
    Entity,
    Inv
}

fn extract_ss(sheet: Sheet, img: &mut RgbaImage, pos: u32) -> RgbaImage {
    let (modulo, size) = match sheet {
        Sheet::Biome => (8, 16),
        Sheet::Entity => (12, 16),
        Sheet::Inv => (32, 32)
    };

    let x = (pos - 1) % modulo;
    let y = (pos - 1) / modulo;

    img.sub_image(x * size, y * size, size, size).to_image()
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // get command args
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
        print_err("not enough arguments");
    }

    let extract_list: HashSet<&'static str> = include_str!("../extract.txt")
        .lines().collect();

    let jarfile = File::open(&args[1])?;
    let reader = BufReader::new(jarfile);
    let mut jar = ZipArchive::new(reader)?;

    let jar_items: Vec<CrunchItem> = (0 .. jar.len()).filter_map(|i| {
        let mut entry = jar.by_index(i).expect("fail read zip");
        let path = entry.enclosed_name().expect("fail zip filename").to_owned();
        let name = path.to_str().expect("fail string convert").to_string();

        if extract_list.contains(name.as_str()) {
            let mut buf: Vec<u8> = Vec::with_capacity(1048576);
            let read = entry.read_to_end(&mut buf).unwrap_or_else(|e| {
                print_err(format!("fail extract: {}\n{}", name, e));
            });

            let img = image::load_from_memory_with_format(
                &buf[..read],
                image::ImageFormat::Png
            ).unwrap_or_else(|e| {
                print_err(format!("fail read image: {}\n{}", name, e));
            });

            if let DynamicImage::ImageRgba8(img) = img {
                print_ok(format!("extracted image: {}", name));
                Some(CrunchItem {
                    image: img,
                    name: path.file_name()
                        .unwrap().to_str()
                        .unwrap().to_string()
                        .strip_suffix(".png").unwrap().to_string()
                })
            } else {
                print_err(format!("could not convert to rgba8: {}", name));
            }
        } else {
            None
        }
    }).collect();
    print_ok("read minecraft jar");

    let mut sheet_biomes = image::open("../sprites/wiki/biomes.png")?.into_rgba8();
    let mut sheet_entity = image::open("../sprites/wiki/entity.png")?.into_rgba8();
    let mut sheet_inv = image::open("../sprites/wiki/inv.png")?.into_rgba8();

    let biomes: Vec<(&'static str, u32)> = vec![
        ("badlands", 12),
        ("badlands_plateau", 50),
        ("bamboo_jungle", 70),
        ("bamboo_jungle_hills", 71),
        ("basalt_deltas", 83),
        ("beach", 16),
        ("birch_forest", 22),
        ("birch_forest_hills", 54),
        ("cold_ocean", 64),
        ("crimson_forest", 80),
        ("dark_forest", 24),
        ("deep_cold_ocean", 65),
        ("deep_frozen_ocean", 57),
        ("deep_lukewarm_ocean", 66),
        ("desert", 2),
        ("desert_hills", 58),
        ("forest", 1),
        ("frozen_river", 15),
        ("giant_tree_taiga", 13),
        ("giant_tree_taiga_hills", 56),
        ("jungle", 5),
        ("jungle_edge", 37),
        ("jungle_hills", 47),
        ("lukewarm_ocean", 67),
        ("mountains", 8),
        ("mushroom_field_shore", 17),
        ("mushroom_fields", 9),
        ("nether_wastes", 10),
        ("plains", 3),
        ("river", 14),
        ("savanna", 23),
        ("savanna_plateau", 51),
        ("snowy_beach", 26),
        ("snowy_mountains", 59),
        ("snowy_taiga", 7),
        ("snowy_taiga_hills", 42),
        ("snowy_tundra", 6),
        ("soul_sand_valley", 82),
        ("stone_shore", 25),
        ("swamp", 4),
        ("taiga", 31),
        ("taiga_hills", 43),
        ("warm_ocean", 69),
        ("warped_forest", 81),
        ("wooded_badlands_plateau", 39),
        ("wooded_hills", 21),
        ("wooded_mountains", 30),
    ];

    let entities: Vec<(&'static str, u32)> = vec![
        ("blaze", 352),
        ("cave_spider", 367),
        ("creeper", 14),
        ("drowned", 133),
        ("elder_guardian", 371),
        ("ender_dragon", 29),
        ("enderman", 21),
        ("endermite", 86),
        ("evoker", 138),
        ("ghast", 329),
        ("guardian", 373),
        ("hoglin", 301),
        ("husk", 447),
        ("magma_cube", 330),
        ("phantom", 125),
        ("piglin", 296),
        ("pillager", 138),
        ("ravager", 137),
        ("shulker", 30),
        ("silverfish", 22),
        ("skeleton", 335),
        ("slime", 340),
        ("spider", 341),
        ("stray", 378),
        ("vex", 380),
        ("vindicator", 381),
        ("witch", 349),
        ("wither", 355),
        ("wither_skeleton", 350),
        ("zoglin", 389),
        ("zombie", 339),
        ("zombie_villager", 227),
        ("zombified_piglin", 342),
        ("bee", 291),
        ("chicken", 327),
        ("cow", 328),
        ("donkey", 359),
        ("fox", 280),
        ("goat", 451),
        ("horse", 358),
        ("llama", 365),
        ("mooshroom", 333),
        ("mule", 366),
        ("ocelot", 345),
        ("panda", 136),
        ("pig", 331),
        ("rabbit", 364),
        ("sheep", 334),
        ("strider", 388),
        ("turtle", 123),
        ("wolf", 338),
        ("tabby", 146),
        ("all_black", 343),
        ("red", 39),
        ("siamese", 347),
        ("british_shorthair", 140),
        ("calico", 141),
        ("persian", 143),
        ("ragdoll", 145),
        ("white", 147),
        ("jellie", 142),
        ("black", 139),
        ("cat", 142),
    ];

    let inv: Vec<(&'static str, u32)> = vec![
        ("dragon_head", 965),
        ("dragon_egg", 3187),
        ("carved_pumpkin", 3411),
        ("red_bed", 3184),
        ("beacon", 3596),
        ("ancient_debris", 134),
        ("end_stone", 3191),
        ("obsidian", 3370),
        ("crying_obsidian", 197),
        ("purpur_block", 910),
        ("grass_block", 981),
        ("target", 196),
        ("honey_block", 107),
        ("hay_bale", 3264),
        ("bee_nest", 64),
        ("potion", 3452),
        ("respawn_anchor", 207),
        ("polished_blackstone", 274),
        ("red_nether_bricks", 1367),
        ("lodestone", 222),
        ("shield", 2527),
        ("nether_bricks", 3385),
        ("netherrack", 3387),
        ("wither_skeleton_skull", 968),
        ("chest", 1239),
        ("enchanted_golden_apple", 261),
        ("ominous_banner", 2468),
    ];

    let biomes = biomes.iter().map(|(path, pos)| {
        print_ok(format!("extract spritesheet image {}", path));
        CrunchItem {
            image: extract_ss(Sheet::Biome, &mut sheet_biomes, *pos),
            name: path.to_string()
        }
    }).collect::<Vec<CrunchItem>>();

    let entities = entities.iter().map(|(path, pos)| {
        print_ok(format!("extract spritesheet image {}", path));
        CrunchItem {
            image: extract_ss(Sheet::Entity, &mut sheet_entity, *pos),
            name: path.to_string()
        }
    }).collect::<Vec<CrunchItem>>();

    let inv = inv.iter().map(|(path, pos)| {
        print_ok(format!("extract spritesheet image {}", path));
        CrunchItem {
            image: extract_ss(Sheet::Inv, &mut sheet_inv, *pos),
            name: path.to_string()
        }
    }).collect::<Vec<CrunchItem>>();

    let items: Vec<CrunchItem> = jar_items.into_iter()
        .chain(biomes.into_iter())
        .chain(entities.into_iter())
        .chain(inv.into_iter())
        .collect();

    let items: Vec<Item<&CrunchItem>> = items.iter().map(|item| {
        Item::new(
            item,
            item.image.width() as usize,
            item.image.height() as usize,
            Rotation::None
        )
    }).collect();

    match crunch::pack_into_po2(1024, items) {
        Ok((w, h, packed)) => {
            print_ok(format!("packed into {}x{} image", w, h));

            let mut atlas: RgbaImage = ImageBuffer::from_fn(
                w as u32, h as u32, |_, _| image::Rgba([0, 0, 0, 0]));

            for (r, i) in &packed {
                atlas.copy_from(&i.image, r.x as u32, r.y as u32).expect("fail copy");
            }

            atlas.save("../sprites/atlas.png").unwrap();
            print_ok("exported atlas");

            let mut meta = String::new();
            for (r, i) in &packed {
                meta.push_str(format!("{},{},{},{},{}\n", r.x, r.y, r.w, r.h, i.name).as_str());
            }

            std::fs::write("../sprites/atlas.txt", meta).expect("failed to write atlas meta");
            print_ok("exported atlas metadata");
        },
        Err(e) => {
            print_err(format!("failed to pack atlas: {:?}", e));
        }
    }

    Ok(())
}
