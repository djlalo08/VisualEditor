use crate::runtime_types::{NodeIndex, OutputIndex, ScopeIdx};
use std::io::Write;
use std::time::Instant;

mod builtins;
mod parse;
mod run;
mod runtime_types;
mod utils;

pub static LOG: bool = true;
pub static LOGFILE: &str = "log.txt";
pub static FILE: &str = "assets/branching.p";

fn main() {
    std::fs::write(LOGFILE, "").expect("Failed to clear logfile");

    let parse = parse::parse(FILE).unwrap();
    log!("\nParsed!\n");

    let last_node = parse.get(0).unwrap().nodes.len() - 1;
    let start = Instant::now();
    run::run_start(&parse, (ScopeIdx(0), NodeIndex(last_node), OutputIndex(0))).unwrap();
    let duration = start.elapsed();
    println!("\nExecution time: {:?}", duration);
}
