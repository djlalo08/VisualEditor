import { mapRepo } from "../MapRepo";
import { getNameAndAttrs } from "./NodeUtils";

export function eval_(ast_node){
    let [name, attrs] = getNameAndAttrs(ast_node);
    console.log(`Evaluating ${name}`);
    switch (name){
        case 'Outs':
        case 'OutBinding':
            return eval_(ast_node.parent);
        case 'InBinding':
            console.log(outBindings);
            console.log(attrs.getvalue);
            console.log(outBindings[attrs.getvalue]);
            return eval_(outBindings[attrs.getvalue]);
        case 'Map':
            let [ins, outs] = ast_node.children;
            console.log(ins);
            ins = ins.children.map(eval_);
            console.log(ins);
            let fn = mapRepo[attrs['name']];
            fn = mapRepo.add;
            return fn(ins);
        case 'Constant':
            return parseInt(attrs.value);
    }
}

let outBindings = {};

export function updateOutbindings(node){
    outBindings = {};
    updateOutbindings_(node);
    console.log(outBindings);
}

function updateOutbindings_(node){
    let [name, attrs] = getNameAndAttrs(node);
    if (name == 'OutBinding'){
        outBindings[attrs.setvalue] = node;
    }

    for (let child of node.children){
        updateOutbindings_(child);
    }
}