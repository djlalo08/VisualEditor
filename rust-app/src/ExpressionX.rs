use crate::compiler::{builtin, ExpressionBody, InputBlock, InputValue, OutputBlock, Value};

#[derive(Debug)]
pub struct Expression<'a> {
    //Basically if we reference an existing expression a bunch of values will be pre-filled. We need to know which is the relevant reference
    pub reference: Option<&'a Expression<'a>>,
    pub ins: InputBlock<'a>,
    pub body: ExpressionBody<'a>,
    //Associates individual results of the expression with the expression's actual return value
    pub outs: OutputBlock,
}

impl Expression<'_> {
    pub fn evaluate(&self) -> Vec<Value> {
        let ins: Vec<_> = self
            .ins
            .input_values
            .iter()
            .map(|x| match x {
                InputValue::ExtExpressionResult {
                    expression,
                    output_idx,
                } => expression.evaluate()[*output_idx],
                InputValue::IntExpressionResult {
                    expression,
                    output_idx,
                } => expression.evaluate()[*output_idx],
                InputValue::Value(val) => *val,
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