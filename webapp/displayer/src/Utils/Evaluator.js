import { mapRepo, specialMapsRepo } from "../MapRepo";
import { getNameAndAttrs } from "./NodeUtils";

let externalMaps = {};
export function evaluate(root, externalMaps_){
    externalMaps = externalMaps_;
    console.log(externalMaps);
    return eval_(root);
}

export function eval_(ast_node){
    let [name, attrs] = getNameAndAttrs(ast_node);
    // console.log(`Evaluating ${name}: ${attrs.name}`);
    let res;
    switch (name){
        case 'Outs':
            return eval_(ast_node.parent);
        case 'OutBinding':
        case 'OutBound':
            return eval_(ast_node.parent)[ast_node.idx];        
        case 'InBinding':
            return eval_(outBindings[attrs.getvalue]);
        case 'Map':
            let [ins, outs] = ast_node.children;
            let result;
            if (attrs.name in mapRepo){
                ins = ins.children.map(eval_);
                let fn = mapRepo[attrs.name];

                let unbounds = ins.filter(x =>x && x.length && x[0] == 'UNBOUND');
                result = unbounds.length? getFunctionPendingBindings(ins, fn): fn(ins);
            }
            if (attrs.name in specialMapsRepo){
                let fn = specialMapsRepo[attrs.name];
                result = fn(ins);
            }
            if (attrs.name in externalMaps){
                ins = ins.children.map(eval_);
                console.log(ins);
                let fn = externalMaps[attrs.name];
                console.log(fn);
                console.log(fn(ins));
                result = fn(ins);
            }
            return attrs.returnidx? result[attrs.returnidx]: result;
        case 'Constant':
            res = eval_constant(attrs.type, attrs.value);
            return attrs.unwrap ? res[0]: res;
        case 'UnBound':
            return ['UNBOUND', attrs.getvalue];
        case 'InBound':
            return ['INBOUND', attrs.getvalue];
        case 'ValueBox':
            return ast_node.supplier();
    }
}

export function getFunctionPendingBindings(ins, fn){
    function myFn(bindings){
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
    return myFn;
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