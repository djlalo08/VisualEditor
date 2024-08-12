use std::collections::HashMap;

struct Lambda<'a> {
    inputs: Vec<InputDef>,
    assigned_inputs: Vec<&'a OutNode<'a>>,
    body: Box<Codeblock<'a>>,
    outs: Vec<OutputDef>,
    id: LambdaId,
}

// this is a union
enum Codeblock<'a> {
    Codeblocks(Vec<Codeblock<'a>>),
    DirCode(Dir, Box<Codeblock<'a>>),
    FnCall(FnCall<'a>),
    FnDef(Lambda<'a>),
}

enum Evaluable<'a> {
    Codeblock(Codeblock<'a>),
    InNode(InNode),
}

struct FnCall<'a> {
//    attrs: Map<String, String>,
    name: String,
    ins: Vec<Evaluable<'a>>,
    outs: Vec<OutNode<'a>>,
    id: FnCallId,

}

enum Dir {
    Hor, Ver
}

struct OutNode<'a> {
    name: String,
    parent: &'a FnCall<'a>,
    index: u8,
}

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

struct InputDef {
    name: String
}

impl InputDef {
    fn from(name: &str) -> InputDef {
        let name = name.to_string();
        InputDef {name}
    }
}

struct OutputDef {
    name: String
}

impl OutputDef {
    fn from(name: &str) -> OutputDef {
        let name = name.to_string();
        OutputDef {name}
    }
}

pub fn myf () {
    println!("Hello world");

    let mut lambda_registry = LambdaRegistry::new();

    let five_out = OutNode::new("5o");
    let five = Evaluable::Codeblock(Codeblock::FnCall(FnCall { 
        name: "5".to_string(), ins: vec![], outs: vec![five_out], id: 17, }));
    let Evaluable::Codeblock(Codeblock::FnCall(FnCall {name: _, ins: _, outs: i, id:_ })) = five else {
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