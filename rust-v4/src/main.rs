use crate::runtime_types::{NodeIndex, ScopeIdx};
use std::io::Write;

mod builtins;
mod parse;
mod run;
mod runtime_types;
mod utils;

fn main() {
    let logfile = "log.txt";
    std::fs::write(logfile, "").expect("Failed to clear logfile");

    let parse = parse::parse("assets/example3.p").unwrap();
    log!("\nParsed!\n");

    let last_node = parse.get(0).unwrap().nodes.len() - 1;
    run::run_start(&parse, (ScopeIdx(0), NodeIndex(last_node))).unwrap();
}
