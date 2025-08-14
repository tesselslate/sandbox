use std::process::Command;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // assemble boot.asm
    let target_dir = std::env::var("OUT_DIR")
        .expect("no OUT_DIR environment variable");

    let obj_path = format!("{}/boot.o", target_dir);
    
    let mut nasm_cmd = Command::new("nasm");
    nasm_cmd.arg("src/boot.asm")
        .arg("-felf64")
        .arg("-o")
        .arg(&obj_path);

    let nasm_out = nasm_cmd.status().expect("failed to run nasm");
    
    if !nasm_out.success() {
        panic!("nasm failed: {}", String::from_utf8_lossy(
            &nasm_cmd.output()
                .expect("failed to get nasm output")
                .stderr
        ));
    }
    
    // link boot.o
    println!("cargo:rustc-link-arg={obj_path}");

    Ok(())
}
