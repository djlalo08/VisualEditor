import { app, updateAST } from '../Actions';
import { mapRepo } from '../MapRepo';
import { addAttr, appendAttrObj, delAttr, getName, makeMap, makeNode } from '../Utils/NodeUtils';
import { handleClose, handleOpen } from './ModalActions';
import { moveUpToVertical } from './NavigationActions';
import { updateSelected } from './SelectionActions';
import { save_snapshot } from './UndoActions';

export function insert_element() {
    handleOpen();
}

export function insertMapFromModal() {
    save_snapshot();

    let { selected, modalText, insertDir } = app.state;

    let name = modalText.trim();
    let mapData = { fn: null };

    if (app.state.irs.hasOwnProperty(name)) {
        mapData = app.state.irs[name];
    } else if (mapRepo.hasOwnProperty(name)) {
        mapData = mapRepo[name];
    }

    let { fn, ...otherData } = mapData;
    let name_split = name.split(' ');
    let m;

    if (name_split[0] == 'c') {
        let objInfo = {
            className: 'constant',
            value: name_split[1],
            type: 'Number',
            hideOuts: 't', returnidx: 0, inline: 't'
        };
        m = makeMap(selected, name_split[1], objInfo);
    } else if (name_split[0] == 'u') {
        m = { value: 'UnBound', parent: selected, children: [] };
        appendAttrObj(m, { className: 'unbound', name: name_split[1], getvalue: name_split[1] });
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
    app.setState({ modalAction: null, insertDir: '' });
    handleClose();
}

function add_right_in(m) {
    let parent_0 = app.state.selected.parent;

    if (!parent_0 || getName(parent_0) != 'Horizontal')
        wrapIn(app.state.selected, { value: 'Horizontal', children: [] });

    let { parent, idx } = app.state.selected;

    insertNode(m, parent, idx + 1);
}

function add_right_out(m) {
    //TODO: Somehow this was never impl'ed?
}

function add_left_in(m) {
    let parent_0 = app.state.selected.parent;

    if (!parent_0 || getName(parent_0) != 'Horizontal')
        wrapIn(app.state.selected, { value: 'Horizontal', children: [] });

    let { parent, idx } = app.state.selected;

    insertNode(m, parent, Math.max(idx - 1, 0));
}

function add_left_out(m) {
    let { parent, idx } = app.state.selected;

    if (parent && getName(parent) == 'Horizontal') {
        insertNode(m, parent, Math.max(idx - 1, 0));
    } else {
        wrapIn(app.state.selected, { value: 'Horizontal', children: [] });
        // add_left(m);
    }
}
function add_next_line(m) {
    let { parent, idx } = app.state.selected;

    if (parent && getName(parent) == 'Vertical') {
        insertNode(m, parent, idx + 1);
    } else {
        wrapIn(app.state.selected, { value: 'Vertical', children: [] });
        add_next_line(m);
    }
}

function add_prev_line(m) {
    let { parent, idx } = app.state.selected;

    if (parent && getName(parent) == 'Vertical') {
        insertNode(m, parent, Math.max(idx - 1, 0));
    } else {
        wrapIn(app.state.selected, { value: 'Vertical', children: [] });
        add_prev_line(m);
    }
}

function wrapIn(toWrap, wrapper) {
    if (!toWrap || !toWrap.parent)
        return; //TODO, we might want to wrap the top-level in some cases

    toWrap.parent.children.splice(toWrap.idx, 1);
    insertNode(wrapper, toWrap.parent, toWrap.idx);
    if (getName(wrapper) == 'Map')
        replaceNode(toWrap, wrapper.children[0].children[0]);

    else
        insertNode(toWrap, wrapper, 0);
}

export function insertNode(node, new_parent, position){
    new_parent.children.splice(position, 0, node);
    for (let [idx, child] of new_parent.children.entries()){
        child.idx = idx;
    }
    
    node.parent = new_parent;
    
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

export function replaceNode(new_node, old_node){
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

export function delete_element(elmt_to_del){
    save_snapshot();

    if (!elmt_to_del)
        return;

    let node = makeNode();
    replaceNode(node, elmt_to_del);
    updateSelected(node);
}