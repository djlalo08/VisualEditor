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
        tabs += '\t';
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