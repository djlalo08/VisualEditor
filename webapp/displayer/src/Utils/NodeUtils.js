import { n_tabs } from "./StringUtils";

export function addAttr(node, key, value) {
    let [name, attrs] = getNameAndAttrs(node);
    attrs[key] = value;
    node.value = name + stringifyAttrs(attrs);
}

export function delAttr(node, key) {
    let [name, attrs] = getNameAndAttrs(node);
    delete attrs[key];
    node.value = name + stringifyAttrs(attrs);
}

export function appendAttrObj(node, new_attrs) {
    let [name, attrs] = getNameAndAttrs(node);
    attrs = { ...attrs, ...new_attrs };
    console.log(attrs);
    node.value = name + stringifyAttrs(attrs);
}

export function stringifyAttrs(attrs) {
    if (!len(attrs))
        return '';

    let attrs_strs = Object.entries(attrs).map(([k, v]) => `${k}:${v}`);
    return '[' + attrs_strs.join(', ') + ']';
}

export function printAst(ast) {
    return _printAst(ast, 0);
}

export function _printAst(ast, depth) {
    let result = '';
    result += n_tabs(depth) + ast.value + '\n';
    for (let child of ast.children) {
        result += _printAst(child, depth + 1);
    }
    return result;
}

function len(obj) {
    return Object.keys(obj).length;
}

export function readAttrs(attrStr) {
    let attrs = {};
    if (!attrStr) return attrs;

    for (let attr of attrStr.split(',')) {
        let attrPair = attr.trim().split(':');
        attrs[attrPair[0]] = attrPair[1];
    }
    return attrs;
}

export function getNameAndAttrsFromStr(str){
    let values = str.split(/[\[\]]/);
    return [values[0], { ...readAttrs(values[1]) }];
}

export function getNameAndAttrs(node) {
    return getNameAndAttrsFromStr(node.value);
}

export function getName(node) {
    return node.value.split(/[\[\]]/)[0];
}

export function updateName(node, newName){
    let attrs = getAttrs(node);
    node.value = newName + stringifyAttrs(attrs);
}

export function getAttrs(node) {
    let values = node.value.split(/[\[\]]/);
    return { ...readAttrs(values[1]) };
}

export function makeMap(parent, name, mapData, id) {
    let { in_num, out_num, ...otherData } = mapData;

    let map = {id, value: `Map[name:${name}]`, idx: 0, parent };
    appendAttrObj(map, otherData);

    let ins = {id:++id, value: 'Ins', idx: 0, parent: map }
    let ins_nodes = [];
    for (let i = 0; i < in_num; i++) {
        ins_nodes.push({id:++id, value: 'Node', idx: i, children: [], parent: ins });
    }

    let outs = {id:++id, value: 'Outs', idx: 1, parent: map }
    let outs_nodes = [];
    for (let i = 0; i < out_num; i++) {
        outs_nodes.push({id: ++id, value: 'Node', idx: i, children: [], parent: outs });
    }

    map.children = [ins, outs];
    ins.children = ins_nodes;
    outs.children = outs_nodes;

    return map;
}

export function makeNode(parent) {
    return { value: 'Node', parent, children: [] };
}

export function getReturns(node) {
    let obg = new ReturnsGetter();
    obg.getReturns(node);
    obg.outBounds.sort(([x, a], [y, b]) => a - b);
    return obg.outBounds.map(([a, _]) => a);
}

class ReturnsGetter {
    constructor() {
        this.outBounds = [];
    }

    getReturns(node) {
        let attrs = getAttrs(node);
        if (attrs.hasOwnProperty('return')) {
            this.outBounds.push([node, attrs.return]);
        }

        for (let child of node.children)
            this.getReturns(child);
    }

}


let inBounds = [];
export function getInBounds(node) {
    inBounds = [];
    getInBounds_(node);
    return inBounds;
}

function getInBounds_(node) {
    if (getName(node) == 'InBound')
        inBounds.push(node);

    for (let child of node.children)
        getInBounds_(child);
}

export function updateInBindings(inBounds, bindings) {
    for (let inBound of inBounds) {
        let { bind_idx } = getAttrs(inBound);
        inBound.supplier = () => bindings[bind_idx];
    }
}

export function getRoot(node) {
    return node.parent ? getRoot(node.parent) : node;
}

export function getFunctions(node){
    let FF = new FunctionsFinder();
    FF.findFunctions(node);
    return FF.functions;
}

class FunctionsFinder {
    constructor() {
        this.functions = {};
        this.findFunctions = this.findFunctions.bind(this);
    }

    findFunctions(node){
        let [name, attrs] = getNameAndAttrs(node);
        if (name == 'MapDef'){
            this.functions[attrs.name] = node;
            return;
        }
        forEach(node, this.findFunctions);
    }
}

export function getImports(root) {
    let IF = new ImportsFinder();
    IF.findImports(root);
    return IF.imports;
}


class ImportsFinder {
    constructor() {
        this.imports = {};
        this.findImports = this.findImports.bind(this);
    }

    findImports(node) {
        let { import_from, name } = getAttrs(node);
        if (import_from && import_from != 'mapRepo')
            this.imports[name] = import_from; //TODO: this needs to really be a unique ID we are holding. What if there are 2 different impls of +, we don't want to use the same import for both
        forEach(node, this.findImports);
    }
}

export function countBounds(root) {
    let BC = new BoundsCounter();
    BC.countBounds(root);
    return [BC.inBounds.size, BC.returns.size];
}

class BoundsCounter {
    constructor() {
        this.inBounds = new Set();
        this.returns = new Set();
        this.countBounds = this.countBounds.bind(this);
    }

    countBounds(node) {
        let [name, attrs] = getNameAndAttrs(node);
        if (name == 'InBound')
            this.inBounds.add(attrs.name);
        if (attrs.hasOwnProperty('return'))
            this.returns.add(attrs.name);
        forEach(node, this.countBounds);
    }
}

export function maxId(node){
    let maxChildId = 0;
    for (let child of node.children || []){
        maxChildId = Math.max(maxChildId, maxId(child));
    }
    return Math.max(node.id, maxChildId);
}

export function forEach(root, fn) {
    for (let child of root.children) {
        fn(child);
        forEach(child, fn);
    }
}