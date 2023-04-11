import { eval_ } from "./Utils/Evaluator";

export const mapRepo = {
    '+': ins => [ins.reduce( (acc, elt) => acc+elt, 0)],
    '*': ins => [ins.reduce( (acc, elt) => acc*elt, 1)],
    '-': ins => [ins[0]- mapRepo['+'](ins.slice(1))],
    '^2': ins => [ins.map(x=>x*x)],
    '√': ins => {let abs = ins.map(x=>Math.sqrt(x)); return [abs, -abs]},
    'id': ins => ins,
    'id2': ins => ins,
    'print': ins => {ins.forEach(x =>  console.log(x));},
    '>': ins => [ins[0]>ins[1]],
    'ls': ins => [ins],
    'map': ins => {console.log(ins[0]); return [ins[0].map(ins[1])]},
    '++': ins => [ins[0]+1],
    'filter': ins => {
        let res = [];
        for (let x of ins[0]){
            if (ins[1](x)[0])
                res.push(x);
        }
        return res;
    },
}

export const specialMapsRepo = {
    'if': ins => {
        let cond = eval_(ins.children[0])[0];
        if (cond)
            return eval_(ins.children[1]);
        else
            return eval_(ins.children[2]);
    },
}