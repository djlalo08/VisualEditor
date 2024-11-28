import { app } from '../Actions';
import { getName } from '../Utils/NodeUtils';
import { updateSelected } from './SelectionActions';

let selectables = ['Map', 'Node', 'InBound', 'MapDef'];
let horizontals = ['Map', 'Node', 'Ins', 'Outs', 'Horizontal', 'InBound'];

export function moveRight(selected) {
    let curr = moveUpToHorizontal(selected);

    if (!curr.parent)
        return;

    if (curr.idx >= curr.parent.children.length - 1) {
        moveRight(curr.parent);
        return;
    }

    let next = curr.parent.children[curr.idx + 1];
    if (selectables.includes(getName(next)))
        updateSelected(next);

    else
        moveDownFrom(next);
}

export function moveLeft(selected) {
    let curr = moveUpToHorizontal(selected);

    if (!curr.parent)
        return;

    if (curr.idx <= 0) {
        moveLeft(curr.parent);
        return;
    }

    let next = curr.parent.children[curr.idx - 1];
    if (selectables.includes(getName(next)))
        updateSelected(next);

    else
        moveDownFrom(next);
}

export function moveUp() {
    let { parent } = app.state.selected;
    while (parent && !selectables.includes(getName(parent)))
        parent = parent.parent;
    updateSelected(parent);
}

export function moveDown() {
    moveDownFrom(app.state.selected);
}

export function moveDownFrom(elmt) {
    if (!hasChildren(elmt))
        return;

    switch (getName(elmt)){
        case 'MapDef':
            let body = elmt.children[2];
            moveDownFrom(body);
            return;
        case 'Map':
            let [ins, outs] = elmt.children;
            if (ins.children.length == 0){
                moveDownFrom(outs);
                return;
            }
    }

    let child = elmt.children[0];

    while (child && !selectables.includes(getName(child))) {
        if (!hasChildren(child)) break;
        child = child.children[0];
    }
    updateSelected(child);
}
function hasChildren(node) {
    return node.children && node.children.length;
}

export function nextLine() {
    _nextLine(app.state.selected);
}
function _nextLine(selected) {
    let curr = moveUpToVertical(selected);
    if (curr.idx >= curr.parent.children.length - 1) {
        if (curr.parent)
            _nextLine(curr.parent);
        return;
    }

    let next = curr.parent.children[curr.idx + 1];
    if (selectables.includes(getName(next)))
        updateSelected(next);

    else
        moveDownFrom(next);
}

export function prevLine() {
    _prevLine(app.state.selected);
}
function _prevLine(selected) {
    let curr = moveUpToVertical(selected);
    if (curr.idx <= 0) {
        if (curr.parent)
            _prevLine(curr.parent);
        return;
    }

    let prev = curr.parent.children[curr.idx - 1];
    if (selectables.includes(getName(prev)))
        updateSelected(prev);

    else
        moveDownFrom(prev);
}
export function moveUpToVertical(node) {
    while (node && node.parent && getName(node.parent) != 'Vertical')
        node = node.parent;
    return node;
}
function moveUpToHorizontal(node) {
    while (node && node.parent && !horizontals.includes(getName(node.parent)))
        node = node.parent;
    return node;
}
