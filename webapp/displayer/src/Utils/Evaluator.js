import { mapRepo, specialMapsRepo } from "../MapRepo";
import { addAttr, getAttrs, getNameAndAttrs, getReturns } from "./NodeUtils";

const VERBOSE = false;

export function evaluate(selected, inBounds, mapRoot, externalMaps){
    let outbindings = updateOutbindings(mapRoot);
    let evaluator = new Evaluationator(inBounds, outbindings, externalMaps);
    return evaluator.evaluate(selected);
}

class Evaluationator {
    constructor(inBounds, outBindings, externalMaps){
        this.inBounds = inBounds;
        this.outBindings = outBindings;
        this.externalMaps = externalMaps;
        this.recusion_count = 0;
        this.cache = {};
        
        this.evaluate = this.evaluate.bind(this);
    }

    evaluate(ast_node){
        let result = this.evaluate_(ast_node);
        addAttr(ast_node, 'result', result);
        let [name, attrs] = getNameAndAttrs(ast_node);
        if (VERBOSE) {
            console.log(ast_node.value);
            console.log(`${name}:${attrs.name} evaluates to :`);
            console.log(result);
            console.log('');
        }
        return result;
    }
    
    evaluate_(ast_node){
        let [name, attrs] = getNameAndAttrs(ast_node);
        // console.log(`Evaluating ${name}: ${attrs.name}`);
        

        switch (name){
            case 'Vertical':
                return this.evaluate(ast_node.children[ast_node.children.length-1]);
            case 'Variable':
            case 'Node':
                if (attrs.hasOwnProperty('getvalue')){
                    return this.evaluate(this.outBindings[attrs.getvalue]);
                }
                return this.evaluate(ast_node.parent)[ast_node.idx];
            case 'Outs':
                return this.evaluate(ast_node.parent);
            case 'Map':
            case 'Constant':
                if (this.cache[ast_node] && attrs.dont_cache != 't' && false){
                    console.log(`${name}: ${attrs.name} has already been evaluated. Using cache value: ${ast_node.cached_result}`);
                    return this.cache[ast_node];
                }

                let result = this.evaluate_map(attrs, ast_node);
                result = attrs.returnidx? result[attrs.returnidx]: result;
                this.cache[ast_node] = result;
                return result;
                case 'UnBound':
                    return ['UNBOUND', attrs.getvalue];
                    case 'InBound':
                        if (ast_node.supplier)
                        return ast_node.supplier();
                    if (attrs.bind_idx)
                    return this.inBounds[attrs.bind_idx];
                return ['INBOUND', attrs.getvalue];
            }
    }
    
    evaluate_map(attrs, ast_node){
        let [ins, outs] = ast_node.children;
        if (attrs.value && attrs.type){
            return [eval_constant(attrs.type, attrs.value)];
        }

        if (attrs.name in mapRepo){
            ins = ins.children.map(this.evaluate);
            let { fn } = mapRepo[attrs.name];
            if (VERBOSE) {
                console.log(`Evaluating map [${attrs.name}] with ins:`);
                ins.forEach(x => console.log(x));
            }

            let unbounds = ins.filter(x => x && x.length && x[0] == 'UNBOUND');
            return unbounds.length? [getFunctionPendingBindings(ins, fn)]: fn(ins);
        }

        let specialMaps = specialMapsRepo(this);
        if (attrs.name in specialMaps){
            let fn = specialMaps[attrs.name];
            return fn(ins.children);
        }

        if (attrs.import_from){
            ins = ins.children.map(this.evaluate);
            
            if (VERBOSE) {
                console.log(`Evaluating map [${attrs.name}] with ins:`);
                // outBindings.forEach(x => console.log(x));
            }
            
            let mapToEval = this.externalMaps[attrs.name];
            let outBounds = getReturns(mapToEval);
            return outBounds.map(outBound => evaluate(outBound, ins, mapToEval, this.externalMaps));
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
        let attrs = getAttrs(node);
        if (attrs.hasOwnProperty('setvalue')){
            this.outBindings[attrs.setvalue] = node;
        }

        for (let child of node.children){
            this.updateOutbindings(child);
        }
        return this.outBindings;
    }
}