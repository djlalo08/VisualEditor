import { mapRepo } from './MapRepo';
import { ast_to_jsx } from './Utils/Converter';
import { parse } from './Utils/IrToAst';
import { updateToMatchLength } from './Utils/ListUtils';
import { addAttr, appendAttrObj, delAttr, getAttrs, getName, makeMap, makeNode, printAst } from './Utils/NodeUtils';

let app = null;
let selectables = ['Map', 'Node', 'InBound', 'OutBound', 'Constant'];
let horizontals = ['Map', 'Node', 'Ins', 'Outs', 'Horizontal', 'InBound', 'OutBound', 'Constant']
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

    let node = makeNode();
    replaceNode(node, elmt_to_del);
    updateSelected(node);
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

    let name = modalText.trim();
    let mapData = {fn:null};
    
    if (app.state.irs.hasOwnProperty(name)){
        mapData = app.state.irs[name];
    } else if (mapRepo.hasOwnProperty(name)){
        mapData = mapRepo[name];
    }

    let { fn, ...otherData } = mapData;
    let name_split = name.split(' ');
    let m;
    
    if (name_split[0] == 'c'){
        m = {value:'Constant', parent:selected, children:[]}
        appendAttrObj(m, { 
            className:'constant', 
            value:name_split[1], name:name_split[1],
            type:'Number', unwrap:'t',
        });
    } else {
        m = makeMap(selected, name, otherData);
    }

    switch (insertDir) {
        case 'In':
            replaceNode(m, selected);
            break;
        case 'Wrap':
            wrapIn(selected, m);
            break;
        case 'Right_Out':
            add_right_out(m);
            break;
        case 'Right_In':
            add_right_in(m);
            break;
        case 'Left_In':
            add_left_in(m);
            break;
        case 'Left_Out':
            add_left_out(m);
            break;
        case 'Down':
            add_next_line(m);
            break;
        case 'Up':
            add_prev_line(m);
            break;
    }
    updateSelected(m);
    app.setState({insertDir: ''});
    handleClose();
}

function add_right_in(m){
    let parent_0  = app.state.selected.parent;
    
    if (!parent_0 || getName(parent_0) != 'Horizontal')
        wrapIn(app.state.selected, {value:'Horizontal', children:[]});

    let {parent, idx} = app.state.selected;

    insertNode(m, parent, idx+1);
}

function add_right_out(m){
    
}

function add_left_in(m){
    let parent_0  = app.state.selected.parent;
    
    if (!parent_0 || getName(parent_0) != 'Horizontal')
        wrapIn(app.state.selected, {value:'Horizontal', children:[]});

    let {parent, idx} = app.state.selected;

    insertNode(m, parent, Math.max(idx-1,0));
}

function add_left_out(m){
    let {parent, idx} = app.state.selected;
    
    if (parent && getName(parent) == 'Horizontal'){
        insertNode(m, parent, Math.max(idx-1, 0));
    } else {
        wrapIn(app.state.selected, {value:'Horizontal', children:[]});
        // add_left(m);
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
    if (!toWrap || !toWrap.parent)
        return //TODO, we might want to wrap the top-level in some cases
    
    toWrap.parent.children.splice(toWrap.idx, 1);
    insertNode(wrapper, toWrap.parent, toWrap.idx);
    if (getName(wrapper) == 'Map')
        replaceNode(toWrap, wrapper.children[0].children[0]);
    else 
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

function replaceNode(new_node, old_node){
    let {idx, parent} = old_node;
    parent.children.splice(idx, 1);
    insertNode(new_node, parent, idx);
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
    if (!imports || !Object.entries(imports).length)
        return;

    for (let [importName, importLocation] of Object.entries(imports)){
        fetch(`${importLocation}${importName}.ir`)
        .then(response => response.text())
        .then(importCode => app.addImport(importName, importCode));
    }
}

export function setMapIns(map, count){
    let [ins, _] = map.children;
    updateToMatchLength(count, ins.children, () => makeNode(ins));
    for (let i = 0; i < ins.children.length; i++){
        ins.children[i].idx = i;
    }
    updateAST();
}

export function incMapIns(map){
    let oldLength = map.children[0].children.length;
    setMapIns(map, oldLength+1);
}

export function decMapIns(map){
    let oldLength = map.children[0].children.length;
    setMapIns(map, oldLength-1);
}