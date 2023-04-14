import { mapRepo, specialMapsRepo } from "../MapRepo";
import { getNameAndAttrs } from "./NodeUtils";

export function evaluate(selected, outBindings, externalMaps){
    let evaluator = new Evaluationator(outBindings, externalMaps);
    return evaluator.evaluate(selected);
}

class Evaluationator {
    constructor(outBindings, externalMaps){
        this.outBindings = outBindings;
        this.externalMaps = externalMaps;
        this.cache = {};
        
        this.evaluate = this.evaluate.bind(this)
    }
    
    evaluate(ast_node){
        let [name, attrs] = getNameAndAttrs(ast_node);
        console.log(`Evaluating ${name}: ${attrs.name}`);
        switch (name){
            case 'Outs':
                return this.evaluate(ast_node.parent);
            case 'OutBinding':
            case 'OutBound':
                return this.evaluate(ast_node.parent)[ast_node.idx];
            case 'InBinding':
                return this.evaluate(this.outBindings[attrs.getvalue]);
            case 'Map':
                let mapval = this.evaluate_map(attrs, ast_node);
                return attrs.returnidx? mapval[attrs.returnidx]: mapval;
            case 'Constant':
                let res = eval_constant(attrs.type, attrs.value);
                return attrs.unwrap ? res[0]: res;
            case 'UnBound':
                return ['UNBOUND', attrs.getvalue];
            case 'InBound':
                return ['INBOUND', attrs.getvalue];
            case 'ValueBox':
                return ast_node.supplier();
        }
    }
    
    evaluate_map(attrs, ast_node){
        let [ins, outs] = ast_node.children;
        if (attrs.recursive){
            let y = 0;
            //TODO figure something out over here...
        }
        if (attrs.name in mapRepo){
            ins = ins.children.map(this.evaluate);
            let fn = mapRepo[attrs.name];

            let unbounds = ins.filter(x =>x && x.length && x[0] == 'UNBOUND');
            return unbounds.length? getFunctionPendingBindings(ins, fn): fn(ins);
        }
        let specialMaps = specialMapsRepo(this);
        if (attrs.name in specialMaps){
            let fn = specialMaps[attrs.name];
            return fn(ins);
        }
        if (attrs.name in this.externalMaps){
            ins = ins.children.map(this.evaluate);
            let fn = this.externalMaps[attrs.name];
            return fn(ins, this.externalMaps);
        }

    }
}

function getFunctionPendingBindings(ins, fn){
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

export function updateOutbindings(root){
    let ob = new OutBinder();
    return ob.updateOutbindings(root);
}

class OutBinder{
    constructor(){
        this.outBindings = {};
        this.updateOutbindings = this.updateOutbindings.bind(this);
    }
    
    updateOutbindings(node){
        let [name, attrs] = getNameAndAttrs(node);
        if (name == 'OutBinding'){
            this.outBindings[attrs.setvalue] = node;
        }

        for (let child of node.children){
            this.updateOutbindings(child);
        }
        return this.outBindings;
    }
}