import { delete_element, enterMoveMode, insertMapFromModal, insert_element, move, moveDown, moveUp, updateSelected } from "./Actions";

const UP = 38;
const DOWN = 40;
const LEFT = 37;
const RIGHT = 39;
const BACKSPACE = 8;
const SPACE = 32;
const ENTER = 13;

const M = 77;

let app = null;

export function keypress(e){
    // console.log(e.keyCode);

    let {selected, showModal} = app.state;

    if (!selected) return;
    if (showModal) {
        if (e.keyCode == ENTER){
            insertMapFromModal();
        }
        return;
    }

    let {parent, children, idx} = selected;
    switch (e.keyCode) {
        case UP:
            moveUp();
            break;
        case DOWN:
            moveDown();
            break;
        case LEFT:
            if (parent && idx > 0) 
                updateSelected(parent.children[idx-1]);
            break;
        case RIGHT:
            if (parent && idx < parent.children.length-1) 
                updateSelected(parent.children[idx+1]);
            break;
        case BACKSPACE:
            delete_element(selected);
            break;
        case SPACE:
            insert_element(selected);
            break;
        case M:
            enterMoveMode();
            break;
        case ENTER:
            move();
            break;
    }
}

export function setApp(_app){
    app = _app; 
}