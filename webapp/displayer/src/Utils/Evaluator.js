import { mapRepo, specialMapsRepo } from "../MapRepo";
import { addAttr, getNameAndAttrs } from "./NodeUtils";

export function evaluate(selected, outBindings, externalMaps){
    let evaluator = new Evaluationator(outBindings, externalMaps);
    return evaluator.evaluate(selected);
}

class Evaluationator {
    constructor(outBindings, externalMaps){
        this.outBindings = outBindings;
        this.externalMaps = externalMaps;
        this.cache = {};
        
        this.evaluate = this.evaluate.bind(this);
    }

    evaluate(ast_node){
        let result = this.evaluate_(ast_node);
        addAttr(ast_node, 'result', result);
        console.log(ast_node.value);
        return result;
    }
    
    evaluate_(ast_node){
        let [name, attrs] = getNameAndAttrs(ast_node);
        // console.log(`Evaluating ${name}: ${attrs.name}`);
        
        switch (name){
            case 'Node':
                if (attrs.hasOwnProperty('getvalue')){
                    return this.evaluate(this.outBindings[attrs.getvalue]);
                }
                return this.evaluate(ast_node.parent)[ast_node.idx];
            case 'Outs':
                return this.evaluate(ast_node.parent);
            case 'OutBinding':
            case 'OutBound':
                let r = this.evaluate(ast_node.parent);
                return r[ast_node.idx];
            case 'InBinding':
                return this.evaluate(this.outBindings[attrs.getvalue]);
            case 'Map':
                if (this.cache[ast_node] && attrs.dont_cache != 't' && false){
                    console.log(`${name}: ${attrs.name} has already been evaluated. Using cache value: ${ast_node.cached_result}`);
                    return this.cache[ast_node];
                }

                let result = this.evaluate_map(attrs, ast_node);
                result = attrs.returnidx? result[attrs.returnidx]: result;
                this.cache[ast_node] = result;
                return result;
            case 'Constant':
                return eval_constant(attrs.type, attrs.value);
            case 'UnBound':
                return ['UNBOUND', attrs.getvalue];
            case 'InBound':
                return ast_node.supplier? ast_node.supplier() :['INBOUND', attrs.getvalue];
        }
    }
    
    evaluate_map(attrs, ast_node){
        let [ins, outs] = ast_node.children;
        if (attrs.name in mapRepo){
            ins = ins.children.map(this.evaluate);
            let { fn } = mapRepo[attrs.name];
            console.log(`Evaluating map: ${attrs.name} with ins: ${ins}`);

            let unbounds = ins.filter(x => x && x.length && x[0] == 'UNBOUND');
            return unbounds.length? [getFunctionPendingBindings(ins, fn)]: fn(ins);
        }

        let specialMaps = specialMapsRepo(this);
        if (attrs.name in specialMaps){
            let fn = specialMaps[attrs.name];
            return fn(ins.children);
        }

        if (attrs.name in this.externalMaps){
            ins = ins.children.map(this.evaluate);
            console.log(`Evaluating map: ${attrs.name} with ins: ${ins}`);
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
            return parseInt(value);
        case 'Boolean':
            return value == 't';
        case 'String':
        default:
            return value;
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
        if (name == 'OutBinding' ||
        (name == 'Node' && attrs.hasOwnProperty('setvalue'))){
            this.outBindings[attrs.setvalue] = node;
        }

        for (let child of node.children){
            this.updateOutbindings(child);
        }
        return this.outBindings;
    }
}