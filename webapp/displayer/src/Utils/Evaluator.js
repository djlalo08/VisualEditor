import { mapRepo, specialMapsRepo } from "../MapRepo";
import { getNameAndAttrs } from "./NodeUtils";

export function eval_(ast_node){
    let [name, attrs] = getNameAndAttrs(ast_node);
    console.log(`Evaluating ${name}: ${attrs.name}`);
    switch (name){
        case 'Outs':
            return eval_(ast_node.parent);
        case 'OutBinding':
            return eval_(ast_node.parent)[ast_node.idx];        
        case 'InBinding':
            return eval_(outBindings[attrs.getvalue]);
        case 'Map':
            let [ins, outs] = ast_node.children;
            if (attrs.name in mapRepo){
                ins = ins.children.map(eval_);

                let fn = mapRepo[attrs.name];

                let unbounds = ins.filter(x => x[0] == 'UNBOUND');
                
                if (unbounds.length){
                    return bindings => {
                        let binding_idx = 0;
                        let new_ins = [];
                        for (let input of ins){
                            if (input[0] != 'UNBOUND'){
                                new_ins.push(input);
                            }
                            else {
                                new_ins.push(bindings[binding_idx]);
                                binding_idx++;
                            }
                        }
                        return fn(new_ins);
                    }
                }

                return fn(ins);
            }
            if (attrs.name in specialMapsRepo){
                let fn = specialMapsRepo[attrs.name];
                return fn(ins);
            }
        case 'Constant':
            switch (attrs.type){
                case 'Number':
                    return [parseInt(attrs.value)];
                case 'Boolean':
                    return [attrs.value == 't'];
                case 'String':
                default:
                    return [attrs.value];
            }
        case 'UnBound':
            return ['UNBOUND', attrs.getvalue];
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