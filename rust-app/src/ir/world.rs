use std::collections::HashMap;

use Types::*;

use crate::compiler::ExpressionId;

use super::*;

#[derive(Debug, PartialEq, Clone)]
pub struct World {
    pub exprs : HashMap<ExpressionId, ExpressionR>,
    max_id : i32,
}

impl World {
    pub fn new() -> Self {
        World {
            exprs: HashMap::new(),
            max_id: -1,
        }
    }

    pub fn new_expr(mut self, ins: InputBlockR, body: ExpressionBodyR, outs: OutputBlockR) -> Self {
        self.max_id +=  1;
        let id = ExpressionId(self.max_id);
        self.exprs.insert(id, ExpressionR {
            reference: None,
            id, ins, body, outs, 
        });
        self 
    }

    pub fn new_empty_expr(mut self) -> Self{
        self.new_expr(
        InputBlockR {
            input_names: vec![],
            input_values: vec![],
        }, 
        ExpressionBodyR::Passthrough,
        OutputBlockR {
            output_names: vec![],
            values: vec![],
        }) 
    }

    pub fn add_expr_to_expr_list(mut self, expr_list: ExpressionId) -> Self {
        self = self.new_empty_expr();

        let mut expr_list = self.exprs.get_mut(&expr_list).expect("Value does not exist");

        match &mut expr_list.body {
            ExpressionBodyR::Expressions {dir, expressions, } => {
                expressions.push(ExpressionId(self.max_id));
            }
            _ => panic!("This is not an expr list"),
        }
        self
    }

    pub fn replace_expr(mut self, old: ExpressionId, mut new: ExpressionR) -> Self {
        new.id = old;
        self.exprs.insert(old, new);
        self
    }
}