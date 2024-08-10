use std::collections::HashMap;
use std::vec;

fn main() {
    let one = Expression {
        reference: None,
        id: ExpressionId(1),
        ins: InputBlock {
            input_names: vec![],
            input_values: vec![],
            input_ids: vec![],
        },
        body: ExpressionBody::Value(Value::Int(1)),
        outs: OutputBlock {
            output_names: vec!["one".to_string()],
            output_ids: vec![OutputId(1)],
            output_associations: HashMap::from([(OutputId(1), OutputValue::Value)]),
            output_values: HashMap::new(),
        },
    };

    let two = Expression {
        reference: None,
        id: ExpressionId(2),
        ins: InputBlock {
            input_names: vec![],
            input_values: vec![],
            input_ids: vec![],
        },
        body: ExpressionBody::Value(Value::Int(2)),
        outs: OutputBlock {
            output_names: vec!["two".to_string()],
            output_ids: vec![OutputId(2)],
            output_associations: HashMap::from([(OutputId(2), OutputValue::Value)]),
            output_values: HashMap::new(),
        },
    };

    let myexpr = Expression {
        reference: None,
        id: ExpressionId(3),
        ins: InputBlock {
            input_names: vec!["".to_string(), "".to_string()],
            input_values: vec![
                InputValue::OutputId(OutputId(1)),
                InputValue::OutputId(OutputId(2)),
            ],
            input_ids: vec![InputId(1), InputId(2)],
        },
        body: ExpressionBody::Builtin(BuiltIn::Add),
        outs: OutputBlock {
            output_names: vec!["result".to_string()],
            output_ids: vec![OutputId(3)],
            output_associations: HashMap::from([(OutputId(3), OutputValue::BuiltIn)]),
            output_values: HashMap::new(),
        },
    };

    let mut exprs = HashMap::from([
        (ExpressionId(1), one),
        (ExpressionId(2), two),
        (ExpressionId(3), myexpr),
    ]);

    let mut input_to_parent =
        HashMap::from([(InputId(1), ExpressionId(3)), (InputId(2), ExpressionId(3))]);

    let mut output_to_parent = HashMap::from([
        (OutputId(1), ExpressionId(1)),
        (OutputId(2), ExpressionId(2)),
        (OutputId(3), ExpressionId(3)),
    ]);

    let mut world = World {
        exprs,
        input_to_parent,
        output_to_parent,
    };

    world.evaluate(ExpressionId(3));
}

struct World {
    exprs: HashMap<ExpressionId, &Expression>,
    input_to_parent: HashMap<InputId, ExpressionId>,
    output_to_parent: HashMap<OutputId, ExpressionId>,
}

impl World {
    fn evaluate(mut self, id: ExpressionId) {
        let mut ins: Vec<&Value> = Vec::new();
        for input_val in &self.exprs.get(&id).unwrap().ins.input_values {
            let result = match input_val {
                InputValue::ExpressionResult {
                    expression,
                    output_id,
                } => todo!(),
                InputValue::Value(val) => &val,
                InputValue::OutputId(id) => {
                    let a = self.output_to_parent.get(&id).unwrap().to_owned();
                    self.evaluate(a);
                    let par = self.exprs.get(&a).unwrap();
                    let result = par.outs.output_values.get(&id).unwrap();
                    result
                }
            };
            ins.push(result);
        }

        match self.exprs.get(&id).unwrap().body {
            ExpressionBody::Builtin(builtin) => match builtin {
                BuiltIn::Add => todo!(),
            },
            ExpressionBody::FnCall { fn_ref } => todo!(),
            ExpressionBody::Dir { dir, body } => todo!(),
            ExpressionBody::Expressions(_) => todo!(),
            ExpressionBody::Value(val) => val,
            ExpressionBody::Passthrough => todo!(),
        };

        let mut expr = self.exprs.get_mut(&id).unwrap();
        expr.outs.output_values = HashMap::new();
    }
}
struct Expression {
    //Basically if we reference an existing expression a bunch of values will be pre-filled. We need to know which is the relevant reference
    reference: Option<ExpressionId>,
    id: ExpressionId,
    ins: InputBlock,
    body: ExpressionBody,
    //Associates individual results of the expression with the expression's actual return value
    outs: OutputBlock,
}

#[derive(PartialEq, Eq, Hash, Clone, Copy)]
struct ExpressionId(i32);

enum ExpressionBody {
    Builtin(BuiltIn),
    FnCall {
        //other metadata would be in this struct body too
        //this has to be a packed expression
        fn_ref: ExpressionId,
    },
    Dir {
        dir: Dir,
        body: Box<ExpressionBody>,
    },
    Expressions(Vec<Expression>),
    Value(Value),
    //This just passes inputs out to outputs.
    //This exists as a way to account for input and output nodes in code
    //It is kind of adding a lot of junk, though, so it would be nice if we could do away with it
    //In other words it's a node, but idk....
    Passthrough,
}

enum BuiltIn {
    Add,
}

enum Dir {
    Hor,
    Ver,
}

struct InputBlock {
    input_names: Vec<String>,
    input_values: Vec<InputValue>,
    input_ids: Vec<InputId>,
}

#[derive(Clone, Copy)]
enum InputValue {
    //It might make sense to consider having such thing as an ExpressionResult type
    ExpressionResult {
        expression: ExpressionId,
        output_id: OutputId,
    },
    Value(Value),
    OutputId(OutputId),
}

#[derive(PartialEq, Eq, Hash, Clone, Copy)]
struct InputId(i32);

struct OutputBlock {
    output_names: Vec<String>,
    //these are global across the program
    output_ids: Vec<OutputId>,
    //Maps each output_id in output_ids to whatever other output location is it coming from
    output_associations: HashMap<OutputId, OutputValue>,
    output_values: HashMap<OutputId, Value>,
}

enum OutputValue {
    OutputId(OutputId),
    BuiltIn,
    Value,
}

#[derive(PartialEq, Eq, Hash, Clone, Copy)]
struct OutputId(i32);

#[derive(Clone, Copy)]
enum Value {
    Int(i32),
    // String(String),
    Float(f64),
    //...
}
