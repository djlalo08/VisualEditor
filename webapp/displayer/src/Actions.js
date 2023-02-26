import { ast_to_jsx } from './Utils/Converter';
import { addAttr, delAttr, getName, makeMap } from './Utils/NodeUtils';

let app = null;
let selectables = ['Map', 'Node'];

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

export function insert_element(node){
    handleOpen();
}

export function handleClose() {
    app.setState({showModal: false, modalText:''});
}

function handleOpen() {
    app.setState({showModal: true});
}

export function insertMapFromModal(){
    let {selected, modalText} = app.state;
    
    if (getName(selected) == 'Node'){
        selected.children.push(makeMap(selected, modalText, 3, 1));
        updateAST();
    }
    handleClose();
}
  
export function updateAST(){
    let JSX = ast_to_jsx(app.state.AST, app.updateSelected)[0];
    app.setState({AST: {...app.state.AST}, JSX});
}

export function enterMoveMode(){
    let {selected, toMove} = app.state;

    if (!selected)
        return;

    if (getName(selected) != 'Map')
        return;
    
    if (toMove){
        delAttr(toMove, 'to_move');
    }
    
    addAttr(selected, 'to_move', 't');
    app.setState({toMove: selected});

    updateAST();
}

export function move(){
    let {selected, toMove} = app.state;

    if (!selected)
        return;
    
    if (!toMove)
        return;
    
    if (getName(selected) != 'Node')
        return;
    
    delete_element(toMove);
    selected.children = [toMove];        
    toMove.parent = selected;
    
    app.setState({toMove: null, selected: toMove});
    delAttr(selected, 'selected');
    addAttr(toMove, 'selected', 't');
    delAttr(toMove, 'to_move');
    
    updateAST();
    
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
    let parent = app.state.selected;
    while (parent && parent.parent && getName(parent.parent) != 'Vertical')
        parent = parent.parent;

    let curr = parent;
    if (curr.idx >= curr.parent.children.length-1)
        return;

    let next = curr.parent.children[curr.idx+1];
    if (selectables.includes(getName(next)))
        updateSelected(next);        
    else
        moveDownFrom(next);
}

export function prevLine(){
    console.log("prevlin");
    let parent = app.state.selected;
    while (parent && parent.parent && getName(parent.parent) != 'Vertical')
        parent = parent.parent;

    let curr = parent;
    if (curr.idx <= 0)
        return;

    let prev = curr.parent.children[curr.idx-1];
    if (selectables.includes(getName(prev)))
        updateSelected(prev);        
    else
        moveDownFrom(prev);
}