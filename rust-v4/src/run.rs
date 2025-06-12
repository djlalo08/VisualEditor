use crate::{
    builtins::{run_builtin, run_special_builintin, SPECIAL_BUILTIN_FNS},
    log,
    runtime_types::{Dag, Frame, Node, NodeIndex, ScopeIdx, Value},
};
use std::collections::VecDeque;
use std::io::Write;

pub(crate) fn run_start(
    dags: &Vec<Dag>,
    entry_point: (ScopeIdx, NodeIndex),
) -> Result<Value, String> {
    let mut frames = VecDeque::new();
    frames.push_back(Frame {
        inputs: vec![],
        cache: vec![],
    });
    run(dags, &mut frames, entry_point, 0)
}

pub fn run(
    dags: &Vec<Dag>,
    frames: &mut VecDeque<Frame>,
    entry_point: (ScopeIdx, NodeIndex),
    d: usize,
) -> Result<Value, String> {
    let (scope_id, node_id) = entry_point;
    log!(d; "{}:{}", scope_id.0, node_id.0);

    let dag = dags
        .get(scope_id.0)
        .ok_or_else(|| format!("Scope with id {} not found", scope_id.0))?;
    let node = dag.nodes.get(node_id.0).unwrap();
    let res = match node {
        Node::FnCall(scope_idx, node_idx) => {
            let inputs = dag.edges.get(node_id.0).unwrap();
            let inputs = inputs
                .into_iter()
                .map(|x| run(dags, frames, (scope_id, x.0), d + 1).unwrap())
                .collect();
            let skips_to = dags
                .get(scope_idx.0)
                .unwrap()
                .edges
                .get(node_idx.0)
                .unwrap();
            if skips_to.len() > 1 {
                panic!("Defns should have exactly one input edge");
            }

            let skips_to = (ScopeIdx(0), skips_to.first().unwrap().0);

            let curr_frame = Frame {
                inputs: inputs,
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
                let r = run_special_builintin(dags, frames, scope_id, node_id, name, d);
                log!(d; " ┗{:?}", r.clone().unwrap_or(Value::Empty));
                return r;
            }
            let inputs = dag.edges.get(node_id.0).unwrap();
            let inputs = inputs
                .into_iter()
                .map(|x| run(dags, frames, (scope_id, x.0), d + 1).unwrap())
                .collect();
            run_builtin(name, inputs)
        }
        Node::Input(scope_idx, node_idx, arg_order) => {
            let edges = dag.edges.get(node_idx.0).unwrap();
            if !edges.is_empty() {
                panic!("Input nodes should not have edges");
            }
            log!(
                d;
                "  arg_order: {arg_order:?}, args: {:?}",
                frames.back().unwrap().inputs
            );
            Ok(frames
                .back()
                .unwrap()
                .inputs
                .get(arg_order.0)
                .cloned()
                .unwrap())
        }
        Node::Defn => Ok(Value::Empty),
    };

    log!(d; " ┗{:?}", res.clone().unwrap_or(Value::Empty));
    res
}
