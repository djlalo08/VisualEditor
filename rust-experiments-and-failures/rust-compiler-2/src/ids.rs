
#[derive(PartialEq, Eq, Hash, Copy, Clone)]
pub struct ParamId(pub usize);

#[derive(PartialEq, Eq, Hash, Copy, Clone)]
pub struct OutNodeId(pub usize);

#[derive(PartialEq, Eq, Hash, Copy, Clone)]
pub struct LambdaId(pub usize);

#[derive(PartialEq, Eq, Hash, Copy, Clone)]
pub struct OutParamId(pub usize);

#[derive(PartialEq, Eq, Hash, Copy, Clone)]
pub struct FnCallId(pub usize);

#[derive(PartialEq, Eq, Hash, Copy, Clone)]
pub struct CodeblockId(pub usize);

#[derive(PartialEq, Eq, Hash, Copy, Clone)]
pub struct EvaluableId(pub usize);

#[derive(PartialEq, Eq, Hash, Copy, Clone)]
pub struct InNodeId (pub usize);
