#![allow(dead_code, unused_variables)]

use std::{fmt::Display, ops::Add};

use crate::Expression::Expression;

//KIDZ RULE! NO PARENTS ALLOWED
//This is an attempt without any access to parents. It actually shouldn't be necessary?
//If expr has a body, those are obv children.
//For inputs:
//if we reference an output, that can be a reference to an arbitrary non-parent expression and output index
//if we nest, we are just looking at children

pub fn doit() {
    let expr1 = Expression {
        reference: None,
        ins: InputBlock {
            input_names: vec!["".to_string(), "".to_string()],
            input_values: vec![
                InputValue::Value(Value::Int(1)),
                InputValue::Value(Value::Int(2)),
            ],
        },
        body: ExpressionBody::Builtin(BuiltIn::Add),
        outs: OutputBlock {
            output_names: vec!["result".to_string()],
            values: vec![],
        },
    };

    let x1 = expr1.evaluate();
    println!("{:?}", x1);

    let expr2 = Expression {
        reference: None,
        ins: InputBlock {
            input_names: vec!["".to_string(), "".to_string()],
            input_values: vec![
                InputValue::Value(Value::Int(2)),
                InputValue::ExtExpressionResult {
                    expression: &expr1,
                    output_idx: 0,
                },
            ],
        },
        body: ExpressionBody::Builtin(BuiltIn::Add),
        outs: OutputBlock {
            output_names: vec!["result".to_string()],
            values: vec![],
        },
    };

    let x2 = expr2.evaluate();
    println!("{:?}", x2);

    let expr3 = Expression {
        reference: None,
        ins: InputBlock {
            input_names: vec!["".to_string(), "".to_string()],
            input_values: vec![
                InputValue::Value(Value::Int(2)),
                InputValue::IntExpressionResult {
                    expression: Expression {
                        reference: None,
                        ins: InputBlock {
                            input_names: vec![],
                            input_values: vec![
                                InputValue::Value(Value::Int(5)),
                                InputValue::Value(Value::Int(5)),
                                InputValue::Value(Value::Int(5)),
                            ],
                        },
                        body: ExpressionBody::Builtin(BuiltIn::Add),
                        outs: OutputBlock {
                            output_names: vec![],
                            values: vec![],
                        },
                    },
                    output_idx: 0,
                },
            ],
        },
        body: ExpressionBody::Builtin(BuiltIn::Add),
        outs: OutputBlock {
            output_names: vec!["result".to_string()],
            values: vec![],
        },
    };

    let x3 = expr3.evaluate();
    println!("{:?}", x3);
}

pub fn builtin(builtin: &BuiltIn, ins: Vec<Value>) -> Vec<Value> {
    match builtin {
        BuiltIn::Add => vec![ins.iter().fold(Value::Int(0), |acc, x| acc + *x)],
    }
}

#[derive(Debug, PartialEq, Eq, Hash, Clone, Copy)]
pub struct ExpressionId(pub i32);

#[derive(Debug)]
pub enum ExpressionBody<'a> {
    Builtin(BuiltIn),
    FnCall {
        //other metadata would be in this struct body too
        //this has to be a packed expression
        fn_ref: ExpressionId,
    },
    Dir {
        dir: Dir,
        body: Box<ExpressionBody<'a>>,
    },
    Expressions(Vec<Expression<'a>>),
    Value(Value),
    //This just passes inputs out to outputs.
    //This exists as a way to account for input and output nodes in code
    //It is kind of adding a lot of junk, though, so it would be nice if we could do away with it
    //In other words it's a node, but idk....
    Passthrough,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum BuiltIn {
    Add,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Dir {
    Hor,
    Ver,
}

#[derive(Debug)]
pub struct InputBlock<'a> {
    input_names: Vec<String>,
    pub input_values: Vec<InputValue<'a>>,
}

#[derive(Debug)]
pub enum InputValue<'a> {
    //It might make sense to consider having such thing as an ExpressionResult type
    ExtExpressionResult {
        expression: &'a Expression<'a>,
        output_idx: usize,
    },
    IntExpressionResult {
        expression: Expression<'a>,
        output_idx: usize,
    },
    Value(Value),
    PackedExpression(&'a Expression<'a>),
}

#[derive(Debug)]
pub struct OutputBlock {
    output_names: Vec<String>,
    //Maps each output_id in output_ids to whatever other output location is it coming from
    values: Vec<Value>,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Value {
    Int(i32),
    // String(String),
    Float(f64),
    //...
}

impl Display for Value {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Value::Int(x) => write!(f, "{x}"),
            Value::Float(x) => todo!(),
        }
    }
}

impl Add for Value {
    type Output = Self;

    fn add(self, rhs: Self) -> Self::Output {
        if std::mem::discriminant(&self) != std::mem::discriminant(&rhs) {
            panic!("Types must match for addition")
        };
        match self {
            Value::Int(x) => match rhs {
                Value::Int(y) => Value::Int(x + y),
                _ => panic!("Types must match for add"),
            },
            Value::Float(x) => match rhs {
                Value::Float(y) => Value::Float(x + y),
                _ => panic!("Types must match for add"),
            },
        }
    }
}