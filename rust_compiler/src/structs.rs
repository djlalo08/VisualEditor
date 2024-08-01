use std::{cell::RefCell, collections::HashMap, hash::Hash, rc::Rc};

use crate::ids::*;

// TODO: When we try to insert an already-existing Id into a registry (using the new methods), panic
// This ensures no overriding or dupes
// Eventually hashmaps will be replaced by vecs with generational ids

type Registry<I,T> = Rc<RefCell<HashMap<I,T>>>;

enum Evaluable {
    L(LambdaId),
    C(CodeblockId),
    F(FnCallId),
    I(InNodeId),
    O(OutNodeId),
    P(ParamId),
    OP(OutParamId),
}

struct Lambda {
    params: Vec<ParamId>,
    args: Vec<Option<CodeblockId>>,
    outs: Vec<OutParamId>,
    body: CodeblockId,
    id: LambdaId,
}

// this is a union
enum Codeblock {
    Codeblocks(Vec<CodeblockId>),
    DirCode(Dir, CodeblockId),
    InNode(InNodeId),
    Param(ParamId),
    FnCall(FnCallId),
    FnDef(LambdaId),
    Primitive(Primitive),
}

#[derive(Clone, Copy)]
enum Primitive {
    Int(i32)
}

struct Cb {
    id: CodeblockId,
    cb: Codeblock,
}

struct FnCall {
    name: String,
    ins: Vec<CodeblockId>,
    outs: Vec<OutNodeId>,
    id: FnCallId,
}

enum Dir {
    Hor, Ver
}

struct OutNode {
    name: String,
    parent: FnCallId,
    id: OutNodeId,
}

enum Refered {
    OutNode(OutNodeId),
    Param(ParamId),
}

struct InNode {
    name: String,
    refers_to: Refered,
    id: InNodeId,
}

struct Param {
    name: String,
    id: ParamId,
}

struct OutParam {
    name: String,
    id: OutParamId,
    refers_to: OutNodeId,
}

struct World {
    lambdas: Registry<LambdaId, Lambda>,
    params : Registry<ParamId, Param>,
    outparams : Registry<OutParamId, OutParam>,
    outnodes : Registry<OutNodeId, OutNode>,
    innodes : Registry<InNodeId, InNode>,
    fn_calls : Registry<FnCallId, FnCall>,
    codeblocks : Registry<CodeblockId, Cb>,
}