export function addAttr(node, key, value){
    let [name, attrs] = getNameAndAttrs(node);
    attrs[key] = value;
    node.value = name + stringifyAttrs(attrs);
}

export function delAttr(node, key){
    let [name, attrs] = getNameAndAttrs(node);
    delete attrs[key];
    node.value = name + stringifyAttrs(attrs);
}

export function stringifyAttrs(attrs){
    if (!len(attrs)) 
        return '';

    let attrs_strs = Object.entries(attrs).map(([k, v]) => `${k}:${v}`);
    return '[' + attrs_strs.join(', ') + ']';
}

export function printAst(ast){
    return _printAst(ast, 0);
}

export function _printAst(ast, depth){
    let result = '';
    result += n_tabs(depth) + ast.value + '\n';
    for (let child of ast.children){
        result += _printAst(child, depth+1);
    }
    return result;
}

function n_tabs(n){
    let tabs = '';
    for (let i = 0; i<n; i++){
        tabs += '    ';
    }
    return tabs;
}

function len(obj){
    return Object.keys(obj).length;
}

export function readAttrs(attrStr){
    let attrs = {};
    if (!attrStr) return attrs;

    for (let attr of attrStr.split(',')){
        let attrPair = attr.trim().split(':');
        attrs[attrPair[0]] = attrPair[1];
    }
    return attrs;
}

export function getNameAndAttrs(node){
    let values = node.value.split(/[\[\]]/);
    return [values[0], {...readAttrs(values[1])}];
}

export function getName(node){
    return node.value.split(/[\[\]]/)[0];
}

export function getAttrs(node){
    let values = node.value.split(/[\[\]]/);
    return {...readAttrs(values[1])};
}

export function makeMap(parent, name, ins_num, outs_num){
    let map = {value: `Map[name:${name}]`, idx:0, parent};

    let ins = {value: 'Ins', idx: 0, parent:map}
    let ins_nodes = [];
    for (let i = 0; i < ins_num; i++){
        ins_nodes.push({value: 'Node', idx:i, children:[], parent:ins});
    }

    let outs = {value: 'Outs', idx: 1, parent:map}
    let outs_nodes = [];
    for (let i = 0; i < outs_num; i++){
        outs_nodes.push({value: 'Node', idx:i, children:[], parent:outs});
    }

    map.children = [ins, outs];
    ins.children = ins_nodes;
    outs.children = outs_nodes;

    return map;
}

export function makeNode(parent){
    return {value:'Node', parent, children:[]};
}

let outBounds = [];
export function getOutBounds(node){
    outBounds = [];
    getOutBounds_(node);
    return outBounds;
}

function getOutBounds_(node){
    if (getName(node) == 'OutBound')
       outBounds.push(node);

    for (let child of node.children)
        getOutBounds_(child);
}

let inBounds = [];
export function getInBounds(node){
    inBounds = [];
    getInBounds_(node);
    return inBounds;
}

function getInBounds_(node){
    if (getName(node) == 'InBound')
       inBounds.push(node);

    for (let child of node.children)
        getInBounds_(child);
}

export function updateInBindings(inBounds, bindings){
    for (let inBound of inBounds){
        let { bind_idx } = getAttrs(inBound);
        inBound.supplier = () => bindings[bind_idx];
    }
}

export function getRoot(node){
    return node.parent? getRoot(node.parent): node;
}

export function getImports(root){
    let IF = new ImportsFinder();
    IF.findImports(root);
    return IF.imports;
}

class ImportsFinder {
    constructor(){
        this.imports = {};
        this.findImports = this.findImports.bind(this);
    }

    findImports(node){
        let {import_from, name} = getAttrs(node);
        if (import_from && import_from != 'mapRepo')
            this.imports[name] = import_from; //TODO: this needs to really be a unique ID we are holding. What if there are 2 different impls of +, we don't want to use the same import for both
        forEach(node, this.findImports);
    }
}

export function countBounds(root){
    let BC = new BoundsCounter();
    BC.countBounds(root);
    return [BC.inBounds.size, BC.outBounds.size];
}

class BoundsCounter {
    constructor(){
        this.inBounds = new Set();
        this.outBounds = new Set();
        this.countBounds = this.countBounds.bind(this);
    }

    countBounds(node) {
        let [name, attrs] = getNameAndAttrs(node);
        if (name == 'InBound')
            this.inBounds.add(attrs.name);
        if (name == 'OutBound')
            this.outBounds.add(attrs.name);
        forEach(node, this.countBounds);
    }
}

export function forEach(root, fn){
    for (let child of root.children){
        fn(child);
        forEach(child, fn);
    }
}