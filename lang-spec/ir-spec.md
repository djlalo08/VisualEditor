Welcome to POO! 

POO is programming language. POO is not ever expected to be written to directly, but rather through a UI above it.
This is a specification for the language itself. This language is found in the IR files (.ir or .poo or .💩). 

This is the CFG for an IR file. Since showing lines and tabs is hard, we will inline everything and use abbrs:
Caps lock are literals, lowercase are grammar items
```cfg
$ -> ROOT dir (codeblock)* 
dir -> [VER] | [HOR]
codeblock -> codeblock codeblock | dir* codeblock | fn_call+ | fn_def+

fn_call -> [MAP] [INS] ([IN_NODE]|codeblock)* [OUTS] [OUT_NODE]*
fn_def -> [MAPDEF] [INS_DEF] [IN_NAME]* [OUT_DEF] [OUT_NAME]* [BODY] codeblock
```

> NOTE: There will probably be some destructuring options, but these are not yet spec'ed

I think that for code-gen directional information can be deleted. If we were using verticality for multi-threading, though, that may no longer be the case...
Also I was thinking that there mgiht be scoping issues, but we have a kinda of "global" scoping, so I think it's actually ok...

I think IN_NODE and OUT_NODE should be different things...
They operate strictly differently and exist in strictly different places in the AST. It is confusing and silly to conflate them.

Variable: Out-nodes can be given varlabels. Having a varlabel makes an outnode a variable. In-nodes can be given a varlabel. Having a varlable makes an innode a variable. If an in-node has a label, then when it is attempted to be evaluated, it looks up out-nodes with labels from the out-nodes table. In practice, it would be very cool to implement this as meta-programming in the language. We can define a macro that finds all varlabelled out-nodes in a file, and finds all varlabelled in-nodes in a file links them together

Fn inputs: In nodes may have no incoming value. Such a node is referred to as an empty node. A function requires all inputs to be bound to be called. When a function is defined (either as a lambda or using mapdef) 

Lambdas: They are just mapdef with the inputs and outputs hidden and used in-place

How do we manually define functions without mapdef? This may have bearing on lambdas, since we want to be able to pass them around as values.

Functions (this is typically done with lambdas) can be packaged. Package is a function that takes a mapdef and returns a single output. That output is a reference to that function, and effectively serves as our way of moving and handling functions "as if they were data". Recall that mapdefs are just creating a complex data-type
Note that function definition actually returns a value -- the function itself! Therefore function definition is secretly a special macro. It takes 3 inputs: 1) input list, 2) fn body list, 3)output list and gives back a function 

Now I'm getting myself comfused and maybe making things a bit overcomplicated. I think there are big decisions to make right now about how functions are defined. From a theoretical perspective, I see functions are just a bunch of calls in some scope that contains 0 or more inputs nodes  with variable types linked to a value that has not yet been defined, and a couple of output nodes specially desigated as nodes. At the same time is a data structure (of calls). I'm now thinking that the true primitive function is the lambda, and function definition is simply a macro that but those lambdas in a global (for the function) namespace.

So what is a lambda, how does it work, and how is it called? 
A lambda is defined by 3 blocks, input, body, output. 
Input specifies the undefined nodes within the lambda that are bound to something evaluable during evaluation.
Body defines the calls that are a part of the lambda
Output defines the values that we are interested in within the lambda

Let's make a lambda type as an example!
Remember, it's a bit funky because is itself a Map which returns a lambda type
Also remember something special happens when a lambda is called -- these unassigned value become linked to something else.

How are lambdas called? We have another special map call runlambda, which takes a lambda and takes the values which will be assigned to the inputs, and gives a list of ouputs as defined by the output section of the lambda.

runlamda itself is defined using 2 more primitive functions: 
First assign, which takes a lambda and some evaluables and gives a copy of that but lambda with some input (or all) to those evaluables.
And next eval which takes a lambda with no unlinked inputs and gives out ouputs based on the relevant output type.

Now let's talk about data structures:

We said a lambda is just a data structure! What does that strcuture look like?
Like so:
```rust
struct Lambda {
    inputs: Vec<INPUT_DEF>;
    body: Codeblock;
    outs: Vec<OUTPUT_DEF>;
}

// this is a union
enum Codeblock {
    Codeblocks(Vec<Codeblock>),
    DirCode(Dir, Codeblock),
    FnCall(FnCall),
    FnDef(Lambda),
}

enum Evaluable {
    Codeblock(Codeblock);
    InNode(InNode);
}

struct FnCall {
    attrs: Map<String, String>;
    ins: Vec<Evaluable>;
    outs: Vec<OutNodes>;
}

enum Dir {
    Hor, Ver;
}

let mylambda = Lambda {
    inputs: vec!["a", "b", "c"];
    body: Codeblock::Codeblocks(vec![
        DirCode(Dir::Hor, //a -b
            FnCall(FnCall {
                attrs: map!["name":"add", "showout":"true"],
                ins: vec![InNode::new("a"), InNode::new("b")],
                outs: vec![OutNode::new("o1")],
            })
        )
        DirCode(Dir::Hor,
            FnCall(FnCall {
                attrs: map!["name":"div", "showout":"true"],
                ins: vec![InNode::new("o1"), InNode::new("c")],
                outs: vec![OutNode::new("res")],
            })
        )
    ])
    outs: vec!["res"];
}
```

Crazy idea: what if my irs are actually just rust code defining rust data structures? This makes compilation super easy, and there is literally no translation involved. The other nice thing here is that it menas syntax highlighting for IRs and all that jazz. It forces a firmly defined IR structure.

Only problem is that it then has to be translated to something webapp can read and interact with. Big sadge. Maybe webasm is the solution here to make _everything_ in rust...

Let me quickly build a POC rust crate that would eval a lambda. Now 