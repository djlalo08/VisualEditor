use std::collections::VecDeque;

use crate::{
    run::run,
    runtime_types::{Dag, Frame, Value},
    NodeIndex, ScopeIdx,
};

pub fn run_builtin(name: &str, inputs: Vec<Value>) -> Result<Value, String> {
    match name {
        "print" => {
            for input in inputs {
                match input {
                    Value::String(s) => println!("{}", s),
                    Value::Int(i) => println!("{}", i),
                    Value::Float(f) => println!("{}", f),
                    Value::Bool(b) => println!("{}", b),
                    Value::List(l) => println!("{:?}", l),
                    Value::Dict(d) => println!("{:?}", d),
                    Value::Empty => println!("Empty"),
                    _ => return Err("Unsupported type for print".to_string()),
                }
            }
            Ok(Value::Empty)
        }
        "+" => {
            let mut sum = 0.0;
            for input in inputs {
                match input {
                    Value::Int(i) => sum += i as f64,
                    Value::Float(f) => sum += f,
                    _ => return Err("Unsupported type for +".to_string()),
                }
            }
            Ok(Value::Float(sum))
        }
        "-" => {
            if inputs.len() != 2 {
                return Err("Subtraction requires exactly 2 inputs".to_string());
            }
            match (&inputs[0], &inputs[1]) {
                (Value::Int(a), Value::Int(b)) => Ok(Value::Int(a - b)),
                (Value::Float(a), Value::Float(b)) => Ok(Value::Float(a - b)),
                _ => Err("Unsupported types for -".to_string()),
            }
        }
        "*" => {
            let mut product = 1.0;
            for input in inputs {
                match input {
                    Value::Int(i) => product *= i as f64,
                    Value::Float(f) => product *= f,
                    _ => return Err("Unsupported type for *".to_string()),
                }
            }
            Ok(Value::Float(product))
        }
        "<=" => {
            if inputs.len() != 2 {
                return Err("Comparison requires exactly 2 inputs".to_string());
            }
            match (&inputs[0], &inputs[1]) {
                (Value::Int(a), Value::Int(b)) => Ok(Value::Bool(a <= b)),
                (Value::Float(a), Value::Float(b)) => Ok(Value::Bool(a <= b)),
                _ => Err("Unsupported types for <=".to_string()),
            }
        }
        _ => Err(format!("Unknown built-in function: {}", name)),
    }
}

pub fn run_special_builintin(
    dags: &Vec<Dag>,
    frames: &mut VecDeque<Frame>,
    scope_id: ScopeIdx,
    node_id: NodeIndex,
    name: &str,
    d: usize,
) -> Result<Value, String> {
    let dag = dags
        .get(scope_id.0)
        .expect("Scope with id not found in DAGs");
    let inputs = dag.edges.get(node_id.0).unwrap();
    match name {
        "if" => {
            if inputs.len() != 3 {
                return Err("if requires exactly 3 inputs".to_string());
            }
            let pred = inputs.get(0).expect("if must have at least one input");
            let pred_val = run(dags, frames, (scope_id, pred.0), d + 1).unwrap();

            match pred_val {
                Value::Bool(true) => run(dags, frames, (scope_id, inputs.get(1).unwrap().0), d + 1),
                Value::Bool(false) => {
                    run(dags, frames, (scope_id, inputs.get(2).unwrap().0), d + 1)
                }
                _ => Err("First input to if must be a boolean".to_string()),
            }
        }
        _ => Err(format!("Unknown special built-in function: {}", name)),
    }
}

pub static SPECIAL_BUILTIN_FNS: &[&str] = &["if"];

pub static BUILTIN_FNS: &[&str] = &[
    "print", "input", "len", "sum", "min", "max", "sorted", "map", "filter", "reduce", "+", "-",
    "*", "/", "%", "==", "!=", "<", ">", "<=", ">=", "and", "or", "not",
];
