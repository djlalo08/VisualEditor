#![allow(dead_code, unused_variables)]

use std::ops::Add;

//KIDZ RULE! NO PARENTS ALLOWED
//This is an attempt without any access to parents. It actually shouldn't be necessary?
//If expr has a body, those are obv children.
//For inputs:
//if we reference an output, that can be a reference to an arbitrary non-parent expression and output index
//if we nest, we are just looking at children

fn main() {
    let mut expr1 = Expression {
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

    let mut expr2 = Expression {
        reference: None,
        ins: InputBlock {
            input_names: vec!["".to_string(), "".to_string()],
            input_values: vec![
                InputValue::Value(Value::Int(2)),
                InputValue::ExpressionResult { expression: &mut expr1, output_idx: 0 }
            ],
        },
        body: ExpressionBody::Builtin(BuiltIn::Add),
        outs: OutputBlock {
            output_names: vec!["result".to_string()],
            values: vec![],
        },
    };

    let x = expr2.evaluate();
    println!("{:?}", x);
}

#[derive(Debug)]
struct Expression<'a> {
    //Basically if we reference an existing expression a bunch of values will be pre-filled. We need to know which is the relevant reference
    reference: Option<&'a Expression<'a>>,
    ins: InputBlock<'a>,
    body: ExpressionBody<'a>,
    //Associates individual results of the expression with the expression's actual return value
    outs: OutputBlock,
}

impl Expression<'_> {
    fn evaluate(&self) -> Vec<Value> {
        let ins: Vec<_> = self
            .ins
            .input_values
            .iter()
            .map(|x| match x {
                InputValue::ExpressionResult {
                    expression,
                    output_idx,
                } => todo!(),
                InputValue::Value(val) => val,
                InputValue::PackedExpression(_) => todo!(),
            })
            .collect();

        match &self.body {
            ExpressionBody::Builtin(b) => builtin(b, ins),
            ExpressionBody::FnCall { fn_ref } => todo!(),
            ExpressionBody::Dir { dir, body } => todo!(),
            ExpressionBody::Expressions(_) => todo!(),
            ExpressionBody::Value(_) => todo!(),
            ExpressionBody::Passthrough => todo!(),
        }
    }
}

fn builtin(builtin: &BuiltIn, ins: Vec<&Value>) -> Vec<Value> {
    match builtin {
        BuiltIn::Add => vec![ins
            .iter()
            .fold(Value::Int(0), |acc, x| acc + **x)
        ],
    }
}

#[derive(Debug, PartialEq, Eq, Hash, Clone, Copy)]
struct ExpressionId(i32);

#[derive(Debug)]
enum ExpressionBody<'a> {
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

#[derive(Debug)]
enum BuiltIn {
    Add,
}

#[derive(Debug)]
enum Dir {
    Hor,
    Ver,
}

#[derive(Debug)]
struct InputBlock<'a> {
    input_names: Vec<String>,
    input_values: Vec<InputValue<'a>>,
}

#[derive(Debug)]
enum InputValue<'a> {
    //It might make sense to consider having such thing as an ExpressionResult type
    ExpressionResult {
        expression: &'a mut Expression<'a>,
        output_idx: i32,
    },
    Value(Value),
    PackedExpression(&'a Expression<'a>),
}

#[derive(Debug)]
struct OutputBlock {
    output_names: Vec<String>,
    //Maps each output_id in output_ids to whatever other output location is it coming from
    values: Vec<Value>,
}

#[derive(Debug, Clone, Copy)]
enum Value {
    Int(i32),
    // String(String),
    Float(f64),
    //...
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