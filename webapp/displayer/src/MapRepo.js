export const mapRepo = {
    '+': ins => [ins.reduce( (acc, elt) => acc+elt, 0)],
    '*': ins => [ins.reduce( (acc, elt) => acc*elt, 1)],
    '-': ins => [ins[0]- mapRepo['+'](ins.slice(1))],
    '^2': ins => [ins.map(x=>x*x)],
    '√': ins => {let abs = ins.map(x=>Math.sqrt(x)); return [abs, -abs]},
    'id': ins => ins,
    'id2': ins => ins,
}