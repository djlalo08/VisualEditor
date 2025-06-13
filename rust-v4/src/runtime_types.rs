#[derive(Debug)]
pub(crate) struct Dag {
    pub nodes: Vec<Node>,
    pub edges: Vec<Vec<(NodeIndex, OutputIndex)>>, // node_idx -> input_idx -> (output_node, output_idx)
}

#[derive(Debug)]
pub(crate) enum Node {
    FnCall(ScopeIdx, NodeIndex),
    Value(Value),
    BuiltIn(String),
    Arg(ArgOrder),
    Defn,
}

#[derive(Debug)]
pub(crate) struct Frame {
    pub args: Vec<Value>,
    pub cache: Vec<Value>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub(crate) struct NodeIndex(pub usize);
impl From<usize> for OutputIndex {
    fn from(value: usize) -> Self {
        OutputIndex(value)
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub(crate) struct InputIndex(pub usize);

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub(crate) struct OutputIndex(pub usize);

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub(crate) struct ScopeIdx(pub usize);

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub(crate) struct ArgOrder(pub usize);

#[derive(Debug, Clone)]
pub(crate) enum Value {
    Empty,
    Int(i64),
    Float(f64),
    String(String),
    Bool(bool),
    List(Vec<Value>),
    Dict(std::collections::HashMap<String, Value>),
}
