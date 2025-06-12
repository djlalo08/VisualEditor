#[derive(Debug)]
pub(crate) struct Dag {
    pub nodes: Vec<Node>,
    pub edges: Vec<Vec<(NodeIndex, OutputIndex)>>,
}

#[derive(Debug)]
pub(crate) enum Node {
    FnCall(ScopeIdx, NodeIndex),
    Value(Value),
    BuiltIn(String),
    Input(ScopeIdx, NodeIndex, ArgOrder),
    Defn,
}

#[derive(Debug)]
pub(crate) struct Frame {
    pub inputs: Vec<Value>,
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
