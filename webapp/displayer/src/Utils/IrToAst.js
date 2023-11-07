import { addAttr, forEach, getName, getNameAndAttrsFromStr, updateName } from "./NodeUtils";
import { indent_level, n_tabs } from "./StringUtils";

export function parse(ir_text){
    let lines = ir_text.split("\n");
    lines = pre_expand(lines);
    let last_indent = 0;
    let root_node = {value: "", children: [], parent: {children: []}, idx: 0};
    let last_node = root_node;
    let line_number = 0;
    for (let line of lines) {
        if (ignore(line)){
            line_number++;
            continue;
        }

        let indent = line.search(/\S/)/4;

        let parent_to_the_node_we_are_adding = last_node;
        for (let i = 0; i <= last_indent-indent; i++){
            parent_to_the_node_we_are_adding = parent_to_the_node_we_are_adding.parent;
        }

        let this_node = {
            value: line.trim(), 
            children: [], 
            parent: parent_to_the_node_we_are_adding,
            id: line_number,
            idx: parent_to_the_node_we_are_adding.children.length,
        };

        parent_to_the_node_we_are_adding.children.push(this_node);

        last_node = this_node; 
        last_indent = indent;
        line_number++;
    };
    root_node = root_node.parent.children[0];
    root_node.parent = null;
    // post_expand(root_node);
    return root_node;
}

function ignore(line){
    return line.trim().startsWith('//') || line.trim().length == 0;
}

function pre_expand(lines){
    let new_lines = [];
    for (let line of lines){
        if (ignore(line)){
            new_lines.push(line);
            continue;
        }

        let [name, attrs] = getNameAndAttrsFromStr(line.trim());
        let indent = indent_level(line);
        if ('Number' == name){
            new_lines.push(`${n_tabs(indent)}Map[name:${attrs.name}, value:${attrs.value}, className:constant, type:Number, inline:t, hide_outs:t, returnidx:0]`);
            new_lines.push(`${n_tabs(indent+1)}Ins`);
            new_lines.push(`${n_tabs(indent+1)}Outs`);
            new_lines.push(`${n_tabs(indent+2)}Node`);
            continue;
        }

                     
        new_lines.push(line);
    }
    return new_lines;
}

function post_expand(node){
    let name = getName(node);
    if ('Constant' == name){
        addAttr(node, 'className', 'constant');
        updateName(node, 'Map');
        let ins = { value: 'Ins', idx:0, parent:node, children:[]};
        let outs = {value: 'Outs', idx:1, parent:node, children:node.children};
        outs.children.forEach(child => child.parent=outs);
        node.children = [ins, outs];
        return;
    }
    forEach(node, post_expand);   
}