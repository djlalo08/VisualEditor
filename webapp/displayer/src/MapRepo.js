
export const mapRepo = {
    '+': ins => [ins.reduce( (acc, elt) => acc+elt, 0)],
    '+!': ins => {
        console.log('logging +'); 
        console.log(ins);
        return [ins.reduce( (acc, elt) => acc+elt, 0)];
    },
    '*': ins => [ins.reduce( (acc, elt) => acc*elt, 1)],
    '-': ins => [ins[0]- mapRepo['+'](ins.slice(1))],
    '^2': ins => ins.map(x=>x*x),
    '√': ins => {let abs = ins.map(x=>Math.sqrt(x)); return [abs, -abs]},
    'id': ins => ins,
    'id2': ins => ins,
    'print': ins => {ins.forEach(x =>  console.log(x));},
    '>': ins => [ins[0]>ins[1]],
    '<': ins => [ins[0]<ins[1]],
    'ls': ins => [ins],
    'map': ins => [ins[0].map(ins[1])],
    '2map': ins => {
        let [as, bs, fn] = ins;
        const n = Math.min(as.length, bs.length);
        let result = [];
        for (let i=0; i<n; i++){
            result.push(fn([as[i], bs[i]]));
        }
        return result;
    },
    'filter': ins => {
        let res = [];
        for (let x of ins[0]){
            if (ins[1](x)[0])
                res.push(x);
        }
        return [res];
    },
    '-1': ins => ins.map(x => x-1),
    // 'inc': ins => [ins.map(x => x+1)],
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