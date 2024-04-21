struct Lambda {
    inputs: Vec<InputDef>,
    body: Box<Codeblock>,
    outs: Vec<OutputDef>,
}

// this is a union
enum Codeblock {
    Codeblocks(Vec<Codeblock>),
    DirCode(Dir, Box<Codeblock>),
    FnCall(FnCall),
    FnDef(Lambda),
}

enum Evaluable {
    Codeblock(Codeblock),
    InNode(InNode),
}

struct FnCall {
//    attrs: Map<String, String>,
    name: String,
    ins: Vec<Evaluable>,
    outs: Vec<OutNode>,
}

enum Dir {
    Hor, Ver
}

struct OutNode {
    name: String
}

impl OutNode {
    fn new(name: &str) -> OutNode {
        let name = name.to_string();
        OutNode {name}
    }
}

struct InNode {
    name: String,
    refers_to: String
}

impl InNode {
    fn new(name: &str, refers_to: &str) -> Evaluable {
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


fn main () {
    println!("Hello world");


    let mylambda = Lambda {
        inputs: vec![
            InputDef::from("a"), 
            InputDef::from("b"), 
            InputDef::from("c")
        ],
        body: Box::new(Codeblock::Codeblocks(vec![
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
        outs: vec![OutputDef::from("res")],
    };
}

