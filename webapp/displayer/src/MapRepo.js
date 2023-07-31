
export const mapRepo = {
    '+': { fn: ins => [ins.reduce( (acc, elt) => acc+elt, 0)] ,
            in_num: 2, out_num: 1, infix:'t', inline:'t', variableinput:'t',
    },
    '+!': { fn: ins => {
            console.log('logging +'); 
            console.log(ins);
            return [ins.reduce( (acc, elt) => acc+elt, 0)];
        },
        in_num: 2, out_num: 1, infix:'t', inline:'t', variableinput:'t',
    },
    '*': { fn: ins => [ins.reduce( (acc, elt) => acc*elt, 1)],
        in_num: 2, out_num: 1, infix:'t', inline:'t', variableinput:'t',
    },
    '-': { fn: ins => [ins[0]- mapRepo['+'](ins.slice(1))],
        in_num: 2, out_num: 1, infix:'t', inline:'t', variableinput:'t',
    },
    '^2': { fn: ins => ins.map(x=>x*x),
        in_num: 1, out_num: 1, postfix:'t', inline:'t',
    },
    '√': { fn: ins => {let abs = ins.map(x=>Math.sqrt(x)); return [abs, -abs]},
        in_num: 1, out_num: 1, prefix:'t', inline:'t',
    },
    'id': { fn: ins => ins },
    'id2': { fn: ins => ins } ,
    'print': { fn:  ins => ins.forEach(x =>  console.log(x))},
    '>': { fn:  ins => [ins[0]>ins[1]],
        in_num: 2, out_num: 1, infix:'t', inline:'t', variableinput:'t',
    },
    '<': { fn:  ins => [ins[0]<ins[1]],
        in_num: 2, out_num: 1, infix:'t', inline:'t', variableinput:'t',
    },
    'ls': { fn:  ins => [ins]},
    'map': { fn:  ins => [ins[0].map(ins[1])]},
    '2map': { fn:  ins => {
        let [as, bs, fn] = ins;
        const n = Math.min(as.length, bs.length);
        let result = [];
        for (let i=0; i<n; i++){
            result.push(fn([as[i], bs[i]]));
        }
        return result;
    } },
    'filter': { fn:  ins => {
            let res = [];
            for (let x of ins[0]){
                if (ins[1](x)[0])
                    res.push(x);
            }
            return [res];
        },
        in_num: 2, out_num:1, underfix:'t', 
    },
    '-1': { fn:  ins => ins.map(x => x-1), 
        in_num: 1, out_num: 1, postfix:'t',
    },
    // 'inc': { fn:  ins => [ins.map(x => x+1)] },
}

export function specialMapsRepo(evaluator) {
    return {
        'if': ins => {
            let cond = evaluator.evaluate(ins.children[0])[0];
            if (cond)
                return evaluator.evaluate(ins.children[1]);
            else
                return evaluator.evaluate(ins.children[2]);
        },
    }
}

export const externalMaps = new Set([
    'inc'
]);