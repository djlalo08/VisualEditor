use std::{cell::RefCell, collections::HashMap, hash::Hash, rc::Rc};

use crate::ids::*;

// TODO: When we try to insert an already-existing Id into a registry (using the new methods), panic
// This ensures no overriding or dupes
// Eventually hashmaps will be replaced by vecs with generational ids

pub type Registry<I,T> = Rc<RefCell<HashMap<I,T>>>;

enum Evaluable {
    L(LambdaId),
    C(CodeblockId),
    F(FnCallId),
    I(InNodeId),
    O(OutNodeId),
    P(ParamId),
    OP(OutParamId),
}

//This is an executable function instance
struct Lambda {
    params: Vec<ParamId>,
    args: Vec<Option<CodeblockId>>,
    outs: Vec<OutParamId>,
    body: CodeblockId,
    id: LambdaId,
}

impl Lambda {
    fn new(
        id: usize, 
        registry: Registry<LambdaId,Lambda>,
        params: Vec<ParamId>,
        outs: Vec<OutParamId>,
        body: CodeblockId,
    ) -> LambdaId {
        let id = LambdaId(id);
        let param_count = params.len();
        let l = Lambda {
            params, outs, body, id,
            args: vec![None; param_count],
        };

        let mut r = (*registry).borrow_mut();
        r.insert(id, l);
        id
    }
}

impl Registered for Lambda {
    type Id = LambdaId;

    fn empty(id: Self::Id) -> Self {
        Lambda {
            params: Vec::new(),
            args: Vec::new(),
            outs: Vec::new(),
            body: CodeblockId(0),
            id,
        }
    }

    fn to_id(id: usize) -> Self::Id { LambdaId(id) }
}


trait Registered where
    Self:Sized {
    type Id: Hash + Eq + PartialEq + Copy + Clone;

    fn register(id: usize, registry: &mut HashMap<Self::Id, Self>) -> Self::Id {
        let id = Self::to_id(id);
        let e = Self::empty(id);
        registry.insert(id, e);
        id
    }

    fn empty(id: Self::Id) -> Self;
    fn to_id(id: usize) -> Self::Id;
}

trait Node {
    fn get_parent(& self) -> & dyn Node;
}
// this is a union
enum    Codeblock {
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
    Int(i32),
    Vec(Vec<Primitive>),
}

struct Cb {
    id: CodeblockId,
    cb: Codeblock,
}

impl Cb {
    fn new(id: usize, registry: Registry<CodeblockId, Cb>, cb: Codeblock) -> CodeblockId {
        let id = CodeblockId(id);
        let c = Cb {
            id,
            cb,
        };
        (*registry).borrow_mut().insert(id, c);
        id
    }

    fn new_innode(
        cb_id: usize, cb_registry: Registry<CodeblockId, Cb>, 
        in_id: usize, in_registry: Registry<InNodeId, InNode>, name: &str, refers_to: Refered
    ) -> CodeblockId {
        Cb::new(cb_id, cb_registry, Codeblock::InNode(
            InNode::new(in_id, in_registry, name, refers_to)))
    }

    fn new_fn_call(
        cb_id: usize, cb_registry: Registry<CodeblockId, Cb>, 
        fn_id: usize, fn_registry: Registry<FnCallId, FnCall>, name: &str, 
        ins: Vec<CodeblockId>,
        outs: Vec<OutNodeId>,
    ) -> CodeblockId {
        Cb::new(cb_id, cb_registry, Codeblock::FnCall(
            FnCall::new(fn_id, fn_registry, name, ins, outs)))
    }
}

impl Registered for Cb {
    type Id = CodeblockId;

    fn empty(id: Self::Id) -> Self { Cb { id, cb: Codeblock::Codeblocks(vec![])} }
    fn to_id(id: usize) -> Self::Id { CodeblockId(id) }
}

struct FnCall {
    name: String,
    ins: Vec<CodeblockId>,
    outs: Vec<OutNodeId>,
    id: FnCallId,
}

impl FnCall {
    fn new(
        id: usize, 
        registry: Registry<FnCallId,FnCall>,
        name: &str,
        ins: Vec<CodeblockId>,
        outs: Vec<OutNodeId>,
    ) -> FnCallId {
        let id = FnCallId(id);
        let f = FnCall { 
            name: name.to_string(), 
            ins,
            outs,
            id,
        };
        (*registry).borrow_mut().insert(id, f);
        id
    }
}

impl Registered for FnCall {
    type Id = FnCallId;

    fn empty(id: Self::Id) -> Self { FnCall { name:String::new(), ins: Vec::new(), outs: Vec::new(), id} }
    fn to_id(id: usize) -> Self::Id { FnCallId(id) }
}

enum Dir {
    Hor, Ver
}

struct OutNode {
    name: String,
    parent: FnCallId,
    id: OutNodeId,
}

impl OutNode {
    fn new(id: usize, registry: Registry<OutNodeId, OutNode>, name: &str, parent: FnCallId) -> OutNodeId {
        let id = OutNodeId(id);
        let o = OutNode {
            name: name.to_string(),
            parent, id
        };
        (*registry).borrow_mut().insert(id, o);
        id
    }
}

impl Registered for OutNode {
    type Id = OutNodeId;

    fn empty(id: Self::Id) -> Self {
        OutNode { name: String::new(), parent: FnCallId(0), id, }
    }
    fn to_id(id: usize) -> Self::Id { OutNodeId(id) }
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

impl InNode {
    fn new(
        id: usize, 
        registry: Registry<InNodeId, InNode>, 
        name: &str,
        refers_to: Refered,
    ) -> InNodeId {
        let id = InNodeId(id);
        let i = InNode {
            name: name.to_string(),
            refers_to, id,
        };
        (*registry).borrow_mut().insert(id, i);
        id
    }
}

impl Registered for InNode {
    type Id = InNodeId;

    fn empty(id: Self::Id) -> Self {
        InNode {
            name: String::new(),
            refers_to: Refered::OutNode(OutNodeId(0)),
            id
        }
    }
    fn to_id(id: usize) -> Self::Id { InNodeId(id) }
}


struct Param {
    name: String,
    id: ParamId,
}

impl Param {
    fn new(id: usize, registry: Registry<ParamId, Param>, name: &str) -> ParamId {
        let id = ParamId(id);
        let p = Param {
            name: name.to_string(),
            id,
        };
        (*registry).borrow_mut().insert(id, p);
        id
    }
}

struct OutParam {
    name: String,
    id: OutParamId,
    refers_to: OutNodeId,
}

impl OutParam {
    fn new(id: usize, registry: Registry<OutParamId, OutParam>, name: &str, refers_to: OutNodeId) -> OutParamId {
        let id = OutParamId(id);
        let o = OutParam {
            name: name.to_string(),
            id, refers_to,
        };
        (*registry).borrow_mut().insert(id, o);
        id
    }
}

impl Registered for Param {
    type Id = ParamId;

    fn empty(id: Self::Id) -> Self {
        Param {
            name: String::new(),
            id,
        }
    }

    fn to_id(id: usize) -> Self::Id {
        ParamId(id)
    }
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

pub fn afn() {

    let lambdas: Registry<LambdaId, Lambda> = Rc::new(RefCell::new(HashMap::new()));
    let params : Registry<ParamId, Param> = Rc::new(RefCell::new(HashMap::new()));
    let outparams : Registry<OutParamId, OutParam> = Rc::new(RefCell::new(HashMap::new()));
    let outnodes : Registry<OutNodeId, OutNode> = Rc::new(RefCell::new(HashMap::new()));
    let innodes : Registry<InNodeId, InNode> = Rc::new(RefCell::new(HashMap::new()));
    let fn_calls : Registry<FnCallId, FnCall> = Rc::new(RefCell::new(HashMap::new()));
    let codeblocks : Registry<CodeblockId, Cb> = Rc::new(RefCell::new(HashMap::new()));

    let w = Rc::new(RefCell::new(World {
        lambdas: Rc::clone(&lambdas),
        params: Rc::clone(&params),
        outparams: Rc::clone(&outparams),
        outnodes: Rc::clone(&outnodes),
        innodes: Rc::clone(&innodes),
        fn_calls: Rc::clone(&fn_calls),
        codeblocks: Rc::clone(&codeblocks),
    }));

    Lambda::new(1, Rc::clone(&lambdas), 
        //ins
        vec![
            Param::new(1, Rc::clone(&params), "a"),
            Param::new(2, Rc::clone(&params), "b"),
            Param::new(3, Rc::clone(&params), "c"),
        ],

        //outs
        vec![OutParam::new(1, Rc::clone(&outparams), "ans", OutNodeId(2))], //Outs should reference internal stuff.

        //body
        Cb::new(1, Rc::clone(&codeblocks), Codeblock::Codeblocks(vec![
            Cb::new(2, Rc::clone(&codeblocks), Codeblock::DirCode(Dir::Hor, 
                Cb::new_fn_call(3, Rc::clone(&codeblocks), 1, Rc::clone(&fn_calls), "add", 
                    //ins
                    vec![
                        Cb::new_innode(4, Rc::clone(&codeblocks), 1, Rc::clone(&innodes), "a", Refered::Param(ParamId(1))),
                        Cb::new_innode(5, Rc::clone(&codeblocks), 2, Rc::clone(&innodes), "b", Refered::Param(ParamId(2))),
                    ], 
    
                    //outs
                    vec![OutNode::new(1, Rc::clone(&outnodes), "o1", FnCallId(1))]
                )
            )),
            Cb::new(6, Rc::clone(&codeblocks), Codeblock::DirCode(Dir::Hor, 
                Cb::new_fn_call(7, Rc::clone(&codeblocks), 2, Rc::clone(&fn_calls), "div", 
                    //ins
                    vec![
                        Cb::new_innode(8, Rc::clone(&codeblocks), 3, Rc::clone(&innodes), "x", Refered::OutNode(OutNodeId(1))),
                        Cb::new_innode(9, Rc::clone(&codeblocks), 4, Rc::clone(&innodes), "c", Refered::Param(ParamId(3))),
                    ], 
    
                    //outs
                    vec![OutNode::new(2, Rc::clone(&outnodes), "res", FnCallId(2))]
                )
            )),
        ]))
    );

    //Apply vals
    lambdas.borrow_mut().get_mut(&LambdaId(1)).unwrap().args = 
        vec![
            Some(Cb::new(10, Rc::clone(&codeblocks), Codeblock::Primitive(Primitive::Int(3)))),
            Some(Cb::new(11, Rc::clone(&codeblocks), Codeblock::Primitive(Primitive::Int(5)))),
            Some(Cb::new(12, Rc::clone(&codeblocks), Codeblock::Primitive(Primitive::Int(2)))),
        ];

    eval(w, L(LambdaId(1)));
}

use Evaluable::*;

fn eval(w: Rc<RefCell<World>>, e: Evaluable) -> Vec<Primitive> {
    let world = (*w).borrow();
    match e {
        L(id) => {
            let ls = (*world.lambdas).borrow();
            let lambda = ls.get(&id).unwrap();
            lambda.outs.iter().map(|out| eval(Rc::clone(&w), OP(*out))[0]).collect()
        },
        C(id) => {
            let cb = world.codeblocks.borrow().get(&id).unwrap();
            vec![]
        },
        F(id) => {
            let ls = (*world.fn_calls).borrow();
            let fn_call = ls.get(&id).unwrap();
            let ins: Vec<Vec<Primitive>> = fn_call.ins.iter().map(|id| eval(Rc::clone(&w), C(*id))).collect();
            match fn_call.name.as_str() {
                "add" => {
                    let Primitive::Int(a) = ins[0];
                    let Primitive::Int(b) = ins[1];
                    vec![Primitive::Int(a+b)]
                },
                "div" => {
                    let Primitive::Int(a) = ins[0];
                    let Primitive::Int(b) = ins[1];
                    vec![Primitive::Int(a/b)]
                }
                _ => vec![]
            }
        },
        I(id) => {
            // let in_node = w.innodes.borrow().get(&id).unwrap();
            vec![]
        },
        O(id) => {
            let ls = (*world.outnodes).borrow();
            let out_node = ls.get(&id).unwrap();
            eval(Rc::clone(&w), F(out_node.parent))
        },
        P(id) => {
            // let param = w.params.borrow().get(&id).unwrap();
            vec![]
        },
        OP(id) => {
            let ls = (*world.outparams).borrow();
            let out_param = ls.get(&id).unwrap();
            eval(Rc::clone(&w), O(out_param.refers_to))
        },
    }

}


// let mylambda = Lambda::new (
//     vec![
//         Param::from("a"), 
//         Param::from("b"), 
//         Param::from("c"),
//     ],
//     Box::new(Codeblock::Codeblocks(vec![
//         Codeblock::DirCode(Dir::Hor, //a -b
//             Box::new(Codeblock::FnCall(FnCall {
//                 name: "add".to_string(),
//                 ins: vec![InNode::new("a", "a"), InNode::new("b", "b")],
//                 outs: vec![OutNode::new("o1")],
//             })
//         )),
//         Codeblock::DirCode(Dir::Hor,
//             Box::new(Codeblock::FnCall(FnCall {
//                 name: "div".to_string(),
//                 // attrs: map!["name":"div", "showout":"true"],
//                 ins: vec![InNode::new("num", "o1"), InNode::new("c", "c")],
//                 outs: vec![OutNode::new("res")],
//             })
//         ))
//     ])),
//     vec![OutputDef::from("res")],
// );