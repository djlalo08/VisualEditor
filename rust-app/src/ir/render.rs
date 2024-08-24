use crate::compiler::{BuiltIn, Dir, ExpressionId, Value};

use super::{world::World, Types::*};

pub fn render() -> World{

    let mut exprs = World::new();
    println!("=======1=========\n{exprs:#?}\n\n");

    exprs = exprs.new_expr(
        InputBlockR {
            input_names: vec![],
            input_values: vec![],
        },
        ExpressionBodyR::Expressions { 
            dir: Dir::Ver,
            expressions: vec![],
        },
        OutputBlockR {
            output_names: vec![],
            values: vec![],
        },
    );
    println!("=======1=========\n{exprs:#?}\n\n");

    exprs = exprs.add_expr_to_expr_list(ExpressionId(0));
    println!("=======1=========\n{exprs:#?}\n\n");

    exprs = exprs.replace_expr(ExpressionId(1), ExpressionR {
        id: ExpressionId(-1),
        reference: None,
        ins: InputBlockR {
            input_names: vec!["a".to_string(), "b".to_string()],
            input_values: vec![],
        },
        body: ExpressionBodyR::Builtin(BuiltIn::Add),
        outs: OutputBlockR { 
            output_names: vec!["c".to_string()], 
            values: vec![],
        }
    });
    println!("=======1=========\n{exprs:#?}\n\n");

    exprs = exprs.add_expr_to_expr_list(ExpressionId(0));
    println!("=======1=========\n{exprs:#?}\n\n");

    exprs = exprs.replace_expr(ExpressionId(2), ExpressionR {
        id: ExpressionId(-1),
        reference: None,
        ins: InputBlockR {
            input_names: vec!["a".to_string(), "b".to_string()],
            input_values: vec![
                InputValueR::Value(Value::Int(6)),
                InputValueR::Value(Value::Int(6)),
                InputValueR::Value(Value::Int(6)),
            ],
        },
        body: ExpressionBodyR::FnCall { fn_ref: ExpressionId(-1), name: "Add".to_string() },
        outs: OutputBlockR { 
            output_names: vec!["c".to_string()], 
            values: vec![],
        }
    });

    exprs
}