import { ast_to_jsx } from './Utils/Converter';
import { parse } from './Utils/IrToAst';
import { addAttr, delAttr, getAttrs, getName, makeMap, printAst } from './Utils/NodeUtils';

let app = null;
let selectables = ['Map', 'Node'];
let horizontals = ['Map', 'Node', 'Ins', 'Outs', 'Horizontal']
const UNDO_LIMIT = 5;

export function setApp(_app){
    app = _app;
}

export function updateSelected(new_selection){
    let {selected} = app.state;
    if (selected) 
        delAttr(selected, 'selected');

    if (selected == new_selection)
        app.setState({selected: null});

    else {
        if (new_selection)
            addAttr(new_selection, 'selected', 't');
        app.setState({selected: new_selection});
    }

    updateAST();
}

export function delete_element(elmt_to_del){
    save_snapshot();

    if (!elmt_to_del)
        return;

    let {parent, idx} = elmt_to_del;

    switch (getName(elmt_to_del)){
        case 'Map':
            parent.children.splice(idx, 1);
            break;
        case 'Node':
            elmt_to_del.children = [];
            break;        
        default:
            return;
    }
    
    updateAST();
}

export function insert_element(){
    handleOpen();
}

export function handleClose() {
    app.setState({showModal: false, modalText:''});
}

function handleOpen() {
    app.setState({showModal: true, modalText:''});
}

export function insertMapFromModal(){
    save_snapshot();

    let {selected, modalText, insertDir} = app.state;
    let [name, in_num, out_num] = modalText.trim().split(' ');
    let m = makeMap(selected, name, in_num, out_num);
    
    switch (insertDir) {
        case '':
            if (getName(selected) == 'Node'){
                selected.children.push(m);
                updateAST();
            }
            break;
        case 'Right':
            add_right(m);
            break;
        case 'Left':
            add_left(m);
            break;
        case 'Down':
            add_next_line(m);
            break;
        case 'Up':
            add_prev_line(m);
            break;
    }
    app.setState({insertDir: ''});
    handleClose();
}

function add_right(m){
    let {parent, idx} = app.state.selected;
    
    if (parent && getName(parent) == 'Horizontal'){
        insertNode(m, parent, idx+1);
    } else {
        let ins = wrapIn(app.state.selected, {value:'Ins', children:[]});
        wrapIn(ins, {value: 'Map[name:id]', children:[]});
        add_right(m);
    }
}

function add_left(m){
    let {parent, idx} = app.state.selected;
    
    if (parent && getName(parent) == 'Horizontal'){
        insertNode(m, parent, Math.max(idx-1, 0));
    } else {
        wrapIn(app.state.selected, {value:'Horizontal', children:[]});
        add_left(m);
    }
    
}

function add_next_line(m){
    let {parent, idx} = app.state.selected;
    
    if (parent && getName(parent) == 'Vertical'){
        insertNode(m, parent, idx+1);
    } else {
        wrapIn(app.state.selected, {value:'Vertical', children:[]});
        add_next_line(m);
    }
}

function add_prev_line(m){
    let {parent, idx} = app.state.selected;
    
    if (parent && getName(parent) == 'Vertical'){
        insertNode(m, parent, Math.max(idx-1, 0));
    } else {
        wrapIn(app.state.selected, {value:'Vertical', children:[]});
        add_prev_line(m);
    }
}

function wrapIn(toWrap, wrapper){
    if (!toWrap.parent)
        return //TODO, we might want to wrap the top-level in some cases
    
    toWrap.parent.children.splice(toWrap.idx, 1);
    insertNode(wrapper, toWrap.parent, toWrap.idx);
    insertNode(toWrap, wrapper, 0);
}
  
export function updateAST(){
    let JSX = ast_to_jsx(app.state.AST)[0];
    app.setState({AST: {...app.state.AST}, JSX});
}

export function secondSelect(){
    let {selected, secondSelect} = app.state;

    if (!selected)
        return;

    if (getName(selected) != 'Map')
        return;
    
    if (secondSelect){
        delAttr(secondSelect, 'second_select');
    }
    
    addAttr(selected, 'second_select', 't');
    app.setState({secondSelect: selected});

    updateAST();
}

export function move(){
    save_snapshot();

    let {selected, secondSelect} = app.state;

    if (!selected)
        return;
    
    if (!secondSelect)
        return;
    
    if (getName(selected) != 'Node')
        return;
    
    delete_element(secondSelect);
    selected.children = [secondSelect];        
    secondSelect.parent = selected;
    
    app.setState({secondSelect: null, selected: secondSelect});
    delAttr(selected, 'selected');
    addAttr(secondSelect, 'selected', 't');
    delAttr(secondSelect, 'second_select');
    
    updateAST();
}

function insertNode(node, new_parent, position){
    new_parent.children.splice(position, 0, node);
    for (let [idx, child] of new_parent.children.entries()){
        child.idx = idx;
    }
    
    node.parent = new_parent;
    
    updateAST();
}

export function extract(){
    save_snapshot();
    
    let {selected} = app.state;
    if (getName(selected) != 'Map')
        return;

    let curr = moveUpToVertical(selected);

    if (curr.idx <= 0){
        delete_element(selected);

        let horizontal = {value:"Horizontal", children:[selected], idx:0};
        insertNode(horizontal, curr.parent, 0) ;
        return;
    }
     
    let prev = curr.parent.children[curr.idx-1];
    delete_element(selected);
    insertNode(selected, prev, 0);
}

export function moveRight(selected){
    let curr = moveUpToHorizontal(selected);

    if (!curr.parent)
        return;

    if (curr.idx >= curr.parent.children.length-1){
        moveRight(curr.parent);
        return;
    }

    let next = curr.parent.children[curr.idx+1];
    if (selectables.includes(getName(next)))
        updateSelected(next);        
    else
        moveDownFrom(next);
}

export function moveLeft(selected){
    let curr = moveUpToHorizontal(selected);

    if (!curr.parent)
        return;

    if (curr.idx <=0){
        moveLeft(curr.parent);
        return;
    }

    let next = curr.parent.children[curr.idx-1];
    if (selectables.includes(getName(next)))
        updateSelected(next);        
    else
        moveDownFrom(next);
}

export function moveUp(){
    let {parent} = app.state.selected;
    while (parent && !selectables.includes(getName(parent)))
        parent = parent.parent;
    updateSelected(parent);
}

export function moveDown(){
    moveDownFrom(app.state.selected);
}

export function moveDownFrom(elmt){
    if (!hasChildren(elmt))
        return;

    let child = elmt.children[0];

    while (child && !selectables.includes(getName(child))){
        if (!hasChildren(child)) break;
        child = child.children[0];
    }
    updateSelected(child);
}

function hasChildren(node){
    return node.children && node.children.length;
}

export function nextLine(){
    _nextLine(app.state.selected);
}

function _nextLine(selected){
    let curr = moveUpToVertical(selected);
    if (curr.idx >= curr.parent.children.length-1){
        if (curr.parent)
            _nextLine(curr.parent);
        return;
    }

    let next = curr.parent.children[curr.idx+1];
    if (selectables.includes(getName(next)))
        updateSelected(next);        
    else
        moveDownFrom(next);
}

export function prevLine(){
    _prevLine(app.state.selected);
}

function _prevLine(selected){
    let curr = moveUpToVertical(selected);
    if (curr.idx <= 0){
        if (curr.parent)
            _prevLine(curr.parent);
        return;
    }

    let prev = curr.parent.children[curr.idx-1];
    if (selectables.includes(getName(prev)))
        updateSelected(prev);        
    else
        moveDownFrom(prev);
}

function moveUpToVertical(node){
    while (node && node.parent && getName(node.parent) != 'Vertical')
        node = node.parent;
    return node;
}

function moveUpToHorizontal(node){
    while (node && node.parent && !horizontals.includes(getName(node.parent)))
        node = node.parent;
    return node;
}

//TODO when lastIRs list goes over UNDO_LIMIT keep only the last UNDO_LIMIT
function save_snapshot(){
    app.state.lastIRs.push(printAst(app.state.AST));
    app.setState({lastIRs: [...app.state.lastIRs], nextIRs: []});
}

export function undo(){
    if (!app.state.lastIRs.length)
        return;
    app.state.nextIRs.push(printAst(app.state.AST));

    let AST = parse(app.state.lastIRs.pop());
    let [JSX, selected] = ast_to_jsx(AST);
    app.setState({AST, JSX, selected, lastIRs: [...app.state.lastIRs], nextIRs: [...app.state.nextIRs]});
}

export function redo(){
    if (!app.state.nextIRs.length)
        return;
    app.state.lastIRs.push(printAst(app.state.AST));
    
    let AST = parse(app.state.nextIRs.pop());
    let [JSX, selected] = ast_to_jsx(AST);
    app.setState({AST, JSX, selected, lastIRs: [...app.state.lastIRs], nextIRs: [...app.state.nextIRs]});
}

export function setToConnect(){
    let {selected} = app.state;

    if (getName(selected) != 'Node')
        return;

    addAttr(selected, 'to_connect', 't');
    app.setState({toConnect: selected});

    updateAST();
}

export function connect(){
    let {selected, toConnect} = app.state;
    
    if (getName(selected) != 'Node')
        return;
    
    let start, end;
    if (getName(selected.parent) == 'Ins' && 
        getName(toConnect.parent) == 'Outs'){
            start = toConnect;
            end = selected;
    }
    else if (getName(selected.parent) == 'Outs' && 
        getName(toConnect.parent) == 'Ins'){
            end = toConnect;
            start = selected;
    }
    else {
        console.log('Invalid node pair for connection was selected');
    }
    
    let startAttrs = getAttrs(start);
    let value = startAttrs.setvalue || startAttrs.id*100;
    
    addAttr(start, 'setvalue', value);
    addAttr(end, 'getvalue', value);

    delAttr(toConnect, 'to_connect', 't');
    app.setState({toConnect: null});

    updateAST();
}

export function openFile(fileName){
    fetch(`./irs/${fileName}.ir`)
    .then(response => response.text())
    .then(text => app.setState(app.stateFromIR(text)));
}

export function loadImports(imports){
    if (!imports || !imports.length)
        return;

    for (let importName of imports){
        fetch(`./irs/${importName}.ir`)
        .then(response => response.text())
        .then(importCode => app.addImport(importName, importCode));
    }
}