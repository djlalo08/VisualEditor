use crate::compiler::{BuiltIn, Dir, ExpressionId, Value};

#[derive(Debug, Clone, PartialEq)]
pub struct ExpressionR {
    pub id: ExpressionId,
    pub reference: Option<ExpressionId>,
    pub ins: InputBlockR,
    pub body: ExpressionBodyR,
    pub outs: OutputBlockR,
}


#[derive(Debug, Clone, PartialEq)]
pub struct InputBlockR {
    pub(crate) input_names: Vec<String>,
    pub input_values: Vec<InputValueR>,
}

#[derive(Debug, Clone, PartialEq)]
pub enum InputValueR {
    //It might make sense to consider having such thing as an ExpressionResult type
    ExtExpressionResult {
        expression: ExpressionId,
        output_idx: usize,
    },
    IntExpressionResult {
        expression: ExpressionId,
        output_idx: usize,
    },
    Value(Value),
    PackedExpression(ExpressionId),
}

#[derive(Debug, Clone, PartialEq)]
pub struct OutputBlockR {
    pub(crate) output_names: Vec<String>,
    //Maps each output_id in output_ids to whatever other output location is it coming from
    pub(crate) values: Vec<Value>,
}

#[derive(Debug, Clone, PartialEq)]
pub enum ExpressionBodyR {
    Builtin(BuiltIn),
    FnCall {
        //other metadata would be in this struct body too
        //this has to be a packed expression
        fn_ref: ExpressionId,
        name: String,
    },
    Expressions {
        dir: Dir,
        expressions: Vec<ExpressionId>,
    },
    Value(Value),
    //This just passes inputs out to outputs.
    //This exists as a way to account for input and output nodes in code
    //It is kind of adding a lot of junk, though, so it would be nice if we could do away with it
    //In other words it's a node, but idk....
    Passthrough,
}