use std::collections::HashMap;

// for now, as a super weird work-around, things dont reference each other,
// they just all have stringed names and global hashmaps? That sounds awful and we 
// lose all of the benefits of a type system. Maybe RC<RefCell> is the way to go? Seems messy...

#[derive(Clone)]
struct Lambda<'a> {
    inputs: Vec<InputDef>,
    assigned_inputs: Vec<&'a OutNode<'a>>,
    body: Box<Codeblock<'a>>,
    outs: Vec<OutputDef>,
    id: LambdaId,
}

struct LambdaRegistry<'a> {
    index: i8,
    registry: HashMap<LambdaId, Lambda<'a>>,
}

impl LambdaRegistry<'_> {
    fn new() -> LambdaRegistry<'static>{
        LambdaRegistry {
            index: 0,
            registry: HashMap::new(),
        }
    }

    fn add(&mut self, mut lambda: Lambda) -> &mut Lambda{
        self.registry.insert(LambdaId::LambdaId(self.index), lambda);
        self.index += 1;
        &mut lambda
    }
}


impl Lambda<'_> {
    fn new<'a>(inputs: Vec<InputDef>, body: Box<Codeblock<'a>>, outs: Vec<OutputDef>, registry: &'a mut LambdaRegistry<'a>) -> &'a mut Lambda<'a>{
        let l = Lambda {
            inputs, body, outs, 
            assigned_inputs: vec![], 
            id: LambdaId::LambdaId(registry.index),
        };
        registry.add(l)
    }
}

#[derive(Clone, Copy, Hash, PartialEq, Eq)]
enum LambdaId {
    LambdaId(i8)
}

// this is a union
#[derive(Clone)]
enum Codeblock<'a> {
    Codeblocks(Vec<Codeblock<'a>>),
    DirCode(Dir, Box<Codeblock<'a>>),
    FnCall(FnCall<'a>),
    FnDef(Lambda<'a>),
}

#[derive(Clone)]
enum Evaluable<'a> {
    Codeblock(Codeblock<'a>),
    InNode(InNode),
}

#[derive(Clone)]
struct FnCall<'a> {
//    attrs: Map<String, String>,
    name: String,
    ins: Vec<Evaluable<'a>>,
    outs: Vec<OutNode<'a>>,
    id: FnCallId,

}

#[derive(Clone, Copy)]
enum FnCallId {
    FnCallId(i8)
}

#[derive(Clone)]
enum Dir {
    Hor, Ver
}

#[derive(Clone)]
struct OutNode<'a> {
    name: String,
    parent: &'a FnCall<'a>,
    index: u8,
}

impl OutNode<'_> {
    fn new<'a>(name: &'a str, parent: &'a FnCall<'a>, index:u8) -> OutNode<'a> {
        let name = name.to_string();
        OutNode {name, parent, index }
    }
}

#[derive(Clone)]
struct InNode {
    name: String,
    refers_to: String
}

impl InNode {
    fn new<'a>(name: &'a str, refers_to: &'a str) -> Evaluable<'a> {
        let name = name.to_string();
        let refers_to = refers_to.to_string();
        Evaluable::InNode(InNode {name, refers_to})
    }
}

#[derive(Clone)]
struct InputDef {
    name: String
}

impl InputDef {
    fn from(name: &str) -> InputDef {
        let name = name.to_string();
        InputDef {name}
    }
}

#[derive(Clone)]
struct OutputDef {
    name: String
}

impl OutputDef {
    fn from(name: &str) -> OutputDef {
        let name = name.to_string();
        OutputDef {name}
    }
}


pub fn fn3 () {
    println!("Hello world");

    let mut lambda_registry = LambdaRegistry::new();

    let five_out = OutNode::new("5o");
    let five = Evaluable::Codeblock(Codeblock::FnCall(FnCall { 
        name: "5".to_string(), ins: vec![], outs: vec![five_out] }));
    let Evaluable::Codeblock(Codeblock::FnCall(FnCall {name: _, ins: _, outs: i})) = five else {
        panic!("Something is wrong")
    };
    let five_out2 = &i[0];

    let mylambda = Lambda::new (
        vec![
            InputDef::from("a"), 
            InputDef::from("b"), 
            InputDef::from("c"),
        ],
        Box::new(Codeblock::Codeblocks(vec![
            Codeblock::DirCode(Dir::Hor, //a -b
                Box::new(Codeblock::FnCall(FnCall {
                    name: "add".to_string(),
                    // attrs: map!["name":"add", "showout":"true"],
                    ins: vec![InNode::new("a", "a"), InNode::new("b", "b")],
                    outs: vec![OutNode::new("o1")],
                })
            )),
            Codeblock::DirCode(Dir::Hor,
                Box::new(Codeblock::FnCall(FnCall {
                    name: "div".to_string(),
                    // attrs: map!["name":"div", "showout":"true"],
                    ins: vec![InNode::new("num", "o1"), InNode::new("c", "c")],
                    outs: vec![OutNode::new("res")],
                })
            ))
        ])),
        vec![OutputDef::from("res")],
        &mut lambda_registry,
    );

    assign(&mylambda, vec![&five_out2, &five_out2, &five_out2]);

}

fn assign<'a>(lambda: &Lambda<'a>, inputs: Vec<&'a OutNode>) -> Lambda<'a>{
    let mut lambda = lambda.clone();
    lambda.assigned_inputs = inputs;
    lambda
}

fn eval<'a>(lambda: &Lambda<'a>) {

}