export function parse(ir_text){
    let lines = ir_text.split("\n");
    let last_indent = 0;
    let root_node = {value: "", children: [], parent: {children: []}};
    let last_node = root_node;
    for (let line of lines) {
        let indent = line.search(/\S/)/4;

        let parent_to_the_node_we_are_adding = last_node;
        for (let i = 0; i <= last_indent-indent; i++){
            parent_to_the_node_we_are_adding = parent_to_the_node_we_are_adding.parent;
        }

        let this_node = {value: line.trim(), children: [], parent: parent_to_the_node_we_are_adding};

        parent_to_the_node_we_are_adding.children.push(this_node);

        last_node = this_node; 
        last_indent = indent;
    };
    return root_node.parent.children[0];
}