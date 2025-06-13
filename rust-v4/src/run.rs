use crate::{
    builtins::{run_builtin, run_special_builintin, SPECIAL_BUILTIN_FNS},
    log,
    runtime_types::{Dag, Frame, Node, NodeIndex, OutputIndex, ScopeIdx, Value},
};
use std::collections::VecDeque;
use std::io::Write;

pub(crate) fn run_start(
    dags: &Vec<Dag>,
    entry_point: (ScopeIdx, NodeIndex, OutputIndex),
) -> Result<Value, String> {
    let mut frames = VecDeque::new();
    frames.push_back(Frame {
        args: vec![],
        cache: vec![],
    });
    run(dags, &mut frames, entry_point, 0)
}

pub fn run(
    dags: &Vec<Dag>,
    frames: &mut VecDeque<Frame>,
    entry_point: (ScopeIdx, NodeIndex, OutputIndex),
    d: usize,
) -> Result<Value, String> {
    let (scope_id, node_id, output_index) = entry_point;
    log!(d; "{}:{}", scope_id.0, node_id.0);

    let dag = dags
        .get(scope_id.0)
        .ok_or_else(|| format!("Scope with id {} not found", scope_id.0))?;
    let node = dag.nodes.get(node_id.0).unwrap();
    let res = match node {
        Node::FnCall(def_scope_idx, def_node_idx) => {
            let inputs = dag.edges.get(node_id.0).unwrap();
            let inputs = inputs
                .into_iter()
                .map(|&(node_id, output_id)| {
                    run(dags, frames, (scope_id, node_id, output_id), d + 1).unwrap()
                })
                .collect();
            let skips_to = *dags
                .get(def_scope_idx.0)
                .unwrap()
                .edges
                .get(def_node_idx.0)
                .unwrap()
                .get(output_index.0)
                .unwrap();

            let skips_to = (*def_scope_idx, skips_to.0, skips_to.1);

            let curr_frame = Frame {
                args: inputs,
                cache: vec![],
            };
            frames.push_back(curr_frame);
            let val = run(dags, frames, skips_to, d + 1);
            frames.pop_back();
            val
        }
        Node::Value(value) => Ok(value.clone()),
        Node::BuiltIn(name) => {
            if SPECIAL_BUILTIN_FNS.contains(&name.as_str()) {
                let r =
                    run_special_builintin(dags, frames, (scope_id, node_id, output_index), name, d);
                log!(d; " ┗{:?}", r.clone().unwrap_or(Value::Empty));
                return r;
            }
            let inputs = dag.edges.get(node_id.0).unwrap();
            let inputs = inputs
                .into_iter()
                .map(|&(node_id, output_id)| {
                    run(dags, frames, (scope_id, node_id, output_id), d + 1).unwrap()
                })
                .collect();
            run_builtin(name, inputs, output_index)
        }
        Node::Arg(arg_order) => {
            log!(
                d;
                "  arg_order: {arg_order:?}, args: {:?}",
                frames.back().unwrap().args
            );
            Ok(frames
                .back()
                .unwrap()
                .args
                .get(arg_order.0)
                .cloned()
                .unwrap())
        }
        Node::Defn => Ok(Value::Empty),
    };

    log!(d; " ┗{:?}", res.clone().unwrap_or(Value::Empty));
    res
}
