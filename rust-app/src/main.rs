#![allow(non_snake_case)]

use compiler::ExpressionId;
use dioxus::prelude::*;
use dioxus_logger::tracing::{info, Level};

mod compiler;
mod Expression;
mod ir;

fn main() {
    // Init logger
    dioxus_logger::init(Level::INFO).expect("failed to init logger");
    info!("starting app");

    dioxus::launch(App);
}

#[component]
fn App() -> Element {
    // Build cool things ✌️
    let world = ir::render();
    let mut z = use_signal(|| 0i32);

    // compiler::doit();

    rsx! {
        link { rel: "stylesheet", href: "main.css" }
        link { rel: "stylesheet", href: "bootstrap-5.3.3-dist/css/bootstrap.css" }
        div { class: "App",
            br {}
            div {
                button { class:"btn btn-primary button", onclick: move |_| z += 1, "{z}"}
                button { class:"btn btn-primary button", "Button 1"}
                button { class:"btn btn-primary button", "Button 1"}
                button { class:"btn btn-primary button", "Button 1"}
            }
            br {}
            h1 { "MyFile.ir" }
            div { crate::ir::Expression {
                world, expression:ExpressionId(0),
            } }
        }
    }
}