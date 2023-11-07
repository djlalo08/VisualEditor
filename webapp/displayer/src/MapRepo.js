
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
    '-': { fn: ins => [ins[0]- ins.slice(1).reduce((acc, elt) => acc+elt, 0)],
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
    '>=': { fn:  ins => [ins[0]>=ins[1]],
        in_num: 2, out_num: 1, infix:'t', inline:'t', variableinput:'t',
    },
    '<': { fn:  ins => [ins[0]<ins[1]],
        in_num: 2, out_num: 1, infix:'t', inline:'t', variableinput:'t',
    },
    '<=': { fn:  ins => [ins[0]<=ins[1]],
        in_num: 2, out_num: 1, infix:'t', inline:'t', variableinput:'t',
    },
    'ls': { fn:  ins => [ins],
        in_num: 2, out_num: 1, prefix:'t', inline:'t', variableinput:'t',
    },
    'map': { fn:  ([ls, fn]) => {
            let res = [];
            for (let item of ls){
                res.push(fn([item])[0]);           
            }
            return [res];
        }
    },
    '2map': { fn:  ins => {
        let [as, bs, fn] = ins;
        const n = Math.min(as.length, bs.length);
        let result = [];
        for (let i=0; i<n; i++){
            result.push(fn([as[i], bs[i]])[0]);
        }
        return [result];
    } },
    'filter': { fn:  ins => {
            let [ls, f] = ins;
            return [ls.filter(x => f([x])[0])];
        },
        in_num: 2, out_num:1, underfix:'t', 
    },
    '-1': { fn:  ins => ins.map(x => x-1), 
        in_num: 1, out_num: 1, postfix:'t',
    },
    'spl': {fn: ins => {
            let ls = ins[0];
            return [ls[0], ls.slice(1)];
        },
        in_num: 1, out_num: 2, underfix:'t',
    },
    '++': { fn: ins => {
            let result = [];
            for (let input of ins) result = result.concat(input);
            return [result];
        },
        in_num: 2, out_num:1, infix:'t', variableinput:'t', inline:'t',
    },
    'isEmpty': { fn: (ins) => [!(ins[0] && ins[0].length)],
        in_num:1, out_num:1, prefix:'t', inline:'t',
    },
    'l1': { fn: ([ls]) => [ls.length <= 1],
        in_num:1, out_num:1, prefix:'t', inline:'t',
    }
    // 'inc': { fn:  ins => [ins.map(x => x+1)] },
}

export function specialMapsRepo(evaluator) {
    return {
        'if': ([cond, then_, else_]) => {
            cond = evaluator.evaluate(cond);
            return  [evaluator.evaluate(cond? then_: else_)];
        },
    }
}

export const externalMaps = new Set([
    'inc'
]);