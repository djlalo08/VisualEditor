use dioxus::prelude::*;
use world::World;
use Types::*;

use crate::compiler::{Dir, ExpressionId};

use super::*;

#[component]
pub fn Expression(world: World, expression: ExpressionId) -> Element {
    let x = world.exprs.get(&expression).expect("Not found");
    let body = x.body.clone();

    // let z = Some(7i32);
    // rsx!(
    //     div {
    //         {match z {
    //             Some(x) => rsx! {p {"example"}},
    //             None => rsx! {p {"nothing"}}
    //         }}

    //     }
    // )
    match body {
        ExpressionBodyR::Builtin(func) => {
            let name = format!("{func:?}");
            rsx! { table { class:"Map", 
                tbody { tr { td { 
                table { tbody { tr {
                for i in x.ins.input_values.clone() {
                    td {InputValue { val:i }}
                }
            }}}
            p { "{name}" }
            }}}}}
        },
        ExpressionBodyR::FnCall { fn_ref, name } => {
            rsx! { table { class:"Map", 
                tbody { tr { td { 
                table { tbody { tr {
                for i in x.ins.input_values.clone() {
                    td {InputValue { val:i }}
                }
            }}}
            p { "{name}" }
            }}}}}
        },
        ExpressionBodyR::Expressions { dir, expressions } => {
            match dir {
                Dir::Hor => {
                    rsx! { table { tr {
                        for ex in expressions {
                            td { Expression { world:world.clone(), expression:ex} }
                        }
                    }}}
                },
                Dir::Ver => {
                    rsx! { table { tbody {
                        for ex in expressions {
                            tr{ td{ Expression { world:world.clone(), expression:ex} }}
                        }
                    }}}
                }
            }
        },
        ExpressionBodyR::Value(x) => {
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

#[component]
pub fn Box(world: World, name: String) -> Element {
    rsx! { 
        table { class:"Map", "{name}" }
    }
}

#[component]
pub fn InputValue(val: InputValueR) -> Element {
    match val {
        InputValueR::ExtExpressionResult { expression, output_idx } => todo!(),
        InputValueR::IntExpressionResult { expression, output_idx } => todo!(),
        InputValueR::Value(x) => {
            rsx! { div {class:"Map io", {format!("{x}")} }}
        },
        InputValueR::PackedExpression(_) => todo!(),
    }
}