use std::{collections::VecDeque, mem};

use crate::{
    run::run,
    runtime_types::{Dag, Frame, Value},
    NodeIndex, OutputIndex, ScopeIdx,
};

pub fn run_builtin(
    name: &str,
    inputs: Vec<Value>,
    output_index: OutputIndex,
) -> Result<Value, String> {
    let mut results = match name {
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
            vec![Value::Empty]
        }
        "+" => {
            let mut sum = 0.0;
            for input in inputs {
                match input {
                    Value::Int(i) => sum += i as f64,
                    Value::Float(f) => sum += f,
                    _ => Err("Unsupported type for +".to_string())?,
                }
            }
            vec![Value::Float(sum)]
        }
        "-" => {
            if inputs.len() != 2 {
                return Err("Subtraction requires exactly 2 inputs".to_string());
            }
            match (&inputs[0], &inputs[1]) {
                (Value::Int(a), Value::Int(b)) => vec![Value::Int(a - b)],
                (Value::Float(a), Value::Float(b)) => vec![Value::Float(a - b)],
                _ => Err("Unsupported types for -".to_string())?,
            }
        }
        "*" => {
            let mut product = 1.0;
            for input in inputs {
                match input {
                    Value::Int(i) => product *= i as f64,
                    Value::Float(f) => product *= f,
                    _ => Err("Unsupported type for *".to_string())?,
                }
            }
            vec![Value::Float(product)]
        }
        "<=" => {
            if inputs.len() != 2 {
                Err("Comparison requires exactly 2 inputs".to_string())?
            }
            match (&inputs[0], &inputs[1]) {
                (Value::Int(a), Value::Int(b)) => vec![Value::Bool(a <= b)],
                (Value::Float(a), Value::Float(b)) => vec![Value::Bool(a <= b)],
                _ => Err("Unsupported types for <=".to_string())?,
            }
        }
        "+-" => {
            if inputs.len() != 1 {
                return Err("+- requires exactly 1 inputs".to_string());
            }
            match &inputs[0] {
                Value::Int(a) => vec![Value::Int(-a), Value::Int(*a)],
                Value::Float(a) => vec![Value::Float(-a), Value::Float(*a)],
                _ => Err("Unsupported types for +-".to_string())?,
            }
        }
        _ => Err(format!("Unknown built-in function: {}", name))?,
    };
    if results.len() <= output_index.0 {
        return Err(format!(
            "Output index {} out of bounds for results of length {}",
            output_index.0,
            results.len()
        ));
    }

    Ok(results.remove(output_index.0))
}

pub fn run_special_builintin(
    dags: &Vec<Dag>,
    frames: &mut VecDeque<Frame>,
    entry_point: (ScopeIdx, NodeIndex, OutputIndex),
    name: &str,
    d: usize,
) -> Result<Value, String> {
    let (scope_id, node_id, output_id) = entry_point;
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
            // Using output index(0) here is probably a bug. User should be able to specify which output index to use.
            let pred_val = run(dags, frames, (scope_id, pred.0, OutputIndex(0)), d + 1).unwrap();

            let mut call = |which: usize| {
                let (input_node, inputs_output_index) =
                    *inputs.get(which).expect("if must have at least two inputs");
                run(
                    dags,
                    frames,
                    (scope_id, input_node, inputs_output_index),
                    d + 1,
                )
            };

            match pred_val {
                Value::Bool(true) => call(1),
                Value::Bool(false) => call(2),
                _ => Err("First input to if must be a boolean".to_string()),
            }
        }
        _ => Err(format!("Unknown special built-in function: {}", name)),
    }
}

pub static SPECIAL_BUILTIN_FNS: &[&str] = &["if"];

pub static BUILTIN_FNS: &[&str] = &[
    "print", "input", "len", "sum", "min", "max", "sorted", "map", "filter", "reduce", "+", "-",
    "*", "+-", "/", "%", "==", "!=", "<", ">", "<=", ">=", "and", "or", "not",
];
