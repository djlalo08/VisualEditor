import { delete_element, enterMoveMode, insertMapFromModal, insert_element, move, moveDown, moveUp, nextLine, prevLine, updateSelected } from "./Actions";

const UP = 38;
const DOWN = 40;
const LEFT = 37;
const RIGHT = 39;
const BACKSPACE = 8;
const SPACE = 32;
const ENTER = 13;
const SHIFT = 16;

const M = 77;
const T = 84;

let app = null;
let held_down = new Set();

export function keyrelease(e){
    held_down.delete(e.keyCode);
}

export function keypress(e){
    // console.log(e.keyCode);
    held_down.add(e.keyCode);

    let {selected, showModal} = app.state;

    if (!selected) return;
    if (showModal) {
        if (e.keyCode == ENTER){
            insertMapFromModal();
        }
        return;
    }

    let {parent, idx} = selected;
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
        case T:
            move();
            break;
        case ENTER:
            if (held_down.has(SHIFT)) 
                prevLine();
            else
                nextLine();
            break;
    }
}

export function setApp(_app){
    app = _app; 
}