use std::collections::HashMap;

use crate::compiler::{BuiltIn, Dir, ExpressionId};

mod Types;
use dioxus::prelude::*;
use dioxus_elements::tbody;
use Types::*;

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
            input_values: vec![],
        },
        body: ExpressionBodyR::FnCall { fn_ref: ExpressionId(-1), name: "Add".to_string() },
        outs: OutputBlockR { 
            output_names: vec!["c".to_string()], 
            values: vec![],
        }
    });

    exprs

}

#[derive(Debug, PartialEq, Clone)]
pub struct World {
    exprs : HashMap<ExpressionId, ExpressionR>,
    max_id : i32,
}

impl World {
    fn new() -> Self {
        World {
            exprs: HashMap::new(),
            max_id: -1,
        }
    }

    fn new_expr(mut self, ins: InputBlockR, body: ExpressionBodyR, outs: OutputBlockR) -> Self {
        self.max_id +=  1;
        let id = ExpressionId(self.max_id);
        self.exprs.insert(id, ExpressionR {
            reference: None,
            id, ins, body, outs, 
        });
        self 
    }

    fn new_empty_expr(mut self) -> Self{
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

    fn add_expr_to_expr_list(mut self, expr_list: ExpressionId) -> Self {
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

    fn replace_expr(mut self, old: ExpressionId, mut new: ExpressionR) -> Self {
        new.id = old;
        self.exprs.insert(old, new);
        self
    }
}

#[component]
pub fn Expression(world: World, expression: ExpressionId) -> Element {
    let x = world.exprs.get(&expression).expect("Not found");
    let b = x.body.clone();

    // let z = Some(7i32);
    // rsx!(
    //     div {
    //         {match z {
    //             Some(x) => rsx! {p {"example"}},
    //             None => rsx! {p {"nothing"}}
    //         }}

    //     }
    // )

    match b {
        ExpressionBodyR::Builtin(func) => {
            let name = format!("{func:?}");
            rsx! { 
                p { "This is my thing {name}" }
            }
        },
        ExpressionBodyR::FnCall { fn_ref, name } => {
            rsx! { 
                p { "{name}" }
            }
        },
        ExpressionBodyR::Expressions { dir, expressions } => {
            match dir {
                Dir::Hor => {
                    rsx! { 
                        p { "This is my thing" }
                    }
                },
                Dir::Ver => {
                    rsx! { table {
                        for ex in expressions {
                            tbody { Expression { world:world.clone(), expression:ex} }
                        }
                    } }
                }
            }
        },
        ExpressionBodyR::Value(_) => {
            rsx! { 
                p { "This is my thing" }
            }
        },
        ExpressionBodyR::Passthrough => {
            rsx! { 
                p { "This is my thing" }
            }
        },
    }

}