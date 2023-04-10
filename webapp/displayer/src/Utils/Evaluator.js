import { mapRepo, specialMapsRepo } from "../MapRepo";
import { getNameAndAttrs } from "./NodeUtils";

export function eval_(ast_node){
    let [name, attrs] = getNameAndAttrs(ast_node);
    console.log(`Evaluating ${name}: ${attrs.name}`);
    switch (name){
        case 'Outs':
            if (attrs.returnidx){
                console.log('this is called');
                return eval_(ast_node.parent)[attrs.returnidx];                
            }

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

                let unbounds = ins.filter(x =>x && x.length && x[0] == 'UNBOUND');
                
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
            const res = eval_constant(attrs.type, attrs.value);
            return attrs.unwrap ? res[0]: res;
        case 'UnBound':
            return ['UNBOUND', attrs.getvalue];
    }
}

function eval_constant(type, value){
    switch (type){
        case 'Number':
            return [parseInt(value)];
        case 'Boolean':
            return [value == 't'];
        case 'String':
        default:
            return [value];
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