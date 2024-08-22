Creating new mappings with more considerations.
We want expressions to be at the forefront. They are easy to reason about:

```rust
struct Expression {
    reference: Option<ExpressionId> //Basically if we reference an existing expression a bunch of values will be pre-filled. We need to know which is the relevant reference
    id: ExpressionId,
    ins: InputBlock,
    body: ExpressionBody,
    outs: OutputBlock, //associates individual results of the expression with the expression's actual return value
}

enum ExpressionBody {
    Builtin(Builtin),
    FnCall {
        fn_ref: ExpressionId, //this could just be the function name or something like that
        //other metadata would be here
    },
    Dir {
        dir: Dir,
        body: ExpressionBody,
    },
    Expressions(Vec<Expression>),
    Value(Value),
}

struct InputBlock {
    input_names: Vec<String>,
    input_values: Vec<InputValue>,
    input_ids: Vec<InputId>
}

struct InputId(i32);

struct OutputBlock {
    output_names: Vec<String>,
    output_ids: Vec<OutputId>, //these are global across the program
    output_associations: Map<OutputId, OutputId> //Maps each output_id in output_ids to whatever other output location is it coming from
}

struct OutputId(i32);

enum Value {
    Int(i32),
    String(String),
    Float(f64),
    ...
    //...
}
```

Can an expression have undefined arguments? I would say yes.

Fn definition _is_ an expression (that returns a function). Typically, this would be used as a lambda.
In one manner of thinking, general global function definitions are just lambdas within the scope of the file. For mental ease of programmer, we might want to represent them visually differently (or maybe not), but in practice, there is no reason implementation needs to be any different.

Put differently, any expression whose expressions body is anything different than a simple function call _is_ a function definition

Visually the intuition is:

|---------------|
|  () () () ()  |
| ------------- |
| StringInHere  |
| ------------- |
|  () () () ()  |
|---------------|

This is an expression. Value is the result of calling StringInHere. In this case, function body _is_ StringInHere. Note that even if some inputs don't have arguments, this is still an expression and a function call (just not a callable expression)


|---------------|
|  () () () ()  |
| ------------- |
| [ ]  [ ]  [ ] |
| ------------- |
|  () () () ()  |
|---------------|

This has boxes in the middle. Those boxes are expressions and values. 
It gets a little confusing here. The top-level expression has the inputs and outputs we see.
How do we get a handle on the generated function itself, though? This might have be different language construct. Let me think on it.

We need a visual element for Expression handles. This is because outputs _should_ live at the level of their expressions, but the expression itself is distinct from its outputs

Let us denote like this:

|---------------|
|  () () () ()  |
| ------------- |
| StringInHere  |
| ------------- |
 \____ ( ) ____/

|---------------|
|  () () () ()  |
| ------------- |
| [ ]  [ ]  [ ] |
| ------------- |
 \____ ( ) ____/

Now a question: does it make sense to have outputs and expression handle at the same time?
Visually: 

|---------------|
|  () () () ()  |
| ------------- |
| StringInHere  |
| ------------- |______
|  () () () ()  |_( )_/
|---------------|

Yes, it does! 
Just these are different instances at different moments.

That is to say, it's all static.
So if we do funny stuff to the expression handle, and also use the outputs, the changes to the expression handle are not affecting the original outputs. But if You unpack the changed expression and use its outputs, then we _are_ using the updated expression

An important thing to note here is that this all cloning and shadowing. The expression coming out of the handle is a _copy_ of the original expression

We can call expression handles by unpacking them:

    |      |
|---|------|----|
|  (•) () (•)   |
| ------------- |
| StringInHere  |
| ------------- |______
|  (•) () () () |_(X)_/       |
|---|-----------|  |          |
    |              |          |
    |            __|__|-------|-------|
    |           /_(X)_|  (A) (•) (B)  |
    |                 | ------------- |
    |                 | StringInHere  |
    |                 | ------------- |
    |                 |  (•) () () () |
    |                 |---|-----------|

Notice that A and B are already defined above, so don't need to be defined again

Also each first output is completely unrelated. If stuff was done to make changes in line 8 of diagram, output of second box would change, but not of first. We never flow upstream!

I'm really liking this. The language has become extremely simple to hold mentally.
Pretty much all we have are expressions, in/out blocks, fn names, and values.

Note that "packing" an expression clones it, but "unpacking" it need not.

A thing to think about in the future is how to handle argument duplication. For a function being recursed or macro'd a lot, with large arguments, cloning the expression whenever packing it might not be ideal

As far as map def, that would just be syntactic sugar for building an expression and mapping it some registry or namespace.  In fact, it might be nice to leave this as explicit. The saving of functions is clearly shown.

One thing to be careful with: if we pack an expression to global namespace, and then later on run an in-place modification on it, and then later call it, since we only copy at packing time, we are at risk of global unexpected modification.


    |      |
|---|------|----|
|  (•) () (•)   |
| ------------- |
| StringInHere  |
| ------------- |______
|  (•) () () () |_(X)_/       |
|---|-----------|  |          |
    |              |          |
                |--|-----|
                | (•)    |
                | ------ |
                | Save X |
                |--------|


|--------|
| Load X |
| ------ |
| (•)    |
|--|-----|
   |
|--|--------------|
| (•)             |
| --------------- |
| In-place modify |
|-----------------|

I think this would effectively not modify X, since in-place modify is never called. This is good, because the language behaves as expected. What we'd really want is:

    |      |
|---|------|----|
|  (•) () (•)   |
| ------------- |
| StringInHere  |
| ------------- |______
|  (•) () () () |_(X)_/       |
|---|-----------|  |          |
    |              |          |
                |--|-----|
                | (•)    |
                | ------ |
                | Save X |
                |--------|


|--------|
| Load X |
| ------ |
| (•)    |
|--|-----|
   |
|--|--------------|
| (•)             |
| --------------- |
| Copy and change |
| --------------- |
| (•)             |
|--|--------------|
   |
|--|-----|
| (•)    |
| ------ |
| Save X |
|--------|

Now X is shadowed with the new version

All we need to write then is:
1. Evaluate
2. Pack
3. Unpack


## Thoughts we didn't go with
    First let's think about the fact that rust hates trees and evaluating parents and such would suck.

    Since we pretty much have only expressions, this ends up fairly simple: expressions all have a unique id.We have a large global map of expressions, and they can freely reference each other. 
    We add in reference rules (only 1 parent, parent must exist, etc) to make sure we always construct a valid tree.

    Using trees in Rust is hard. In particular, it seems like navigating up to find parents is hard. One idea is we can invert the tree when we want to evaluate -- that is a make a copy with all ownership directions flipped... Problem is if node has 2 children, when flipped, who owns the parent?

    Second idea -- Make an n-ary expression tree. That way it's just a vec and we can just do math to locate parents/children...

## Separate compilation from IR AST

We were successful in building an IR that is is Rust friendly. It uses references to expressions and it is all owned by a root expression. We like direct references for evaluation speed. However, this won't work. Using references results in lifetime pollution, which in turn doesn't play nice with dioxus

Solution: 2 separate structures. 
First structure everything is flat and based on id relations (or maybe a path, not sure which is better).
Then compilation takes this tree and transforms it into a tree with direct ownership. Lifetime annotations are ok here. The other reason this is nice is that we can do _real_ compilation which can involve unpacking expressions and stuff like that. This will keep code reasonably fast.