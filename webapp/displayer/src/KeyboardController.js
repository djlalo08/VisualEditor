import * as a from "./Actions";

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
const E = 69;
const Z = 90;
const A = 65;
const D = 68;
const W = 87;
const S = 83;
const C = 67;

let app = null;
let held_down = new Set();

export function keyrelease(e){
    held_down.delete(e.keyCode);
}

export function keypress(e){
    // console.log(e.keyCode);
    held_down.add(e.keyCode);
    if (!app.state.showModal)
        e.preventDefault();

    let {selected, showModal} = app.state;

    if (!selected) return;
    if (showModal) {
        if (e.keyCode == ENTER){
            a.insertMapFromModal();
        }
        return;
    }

    switch (e.keyCode) {
        case UP:
            a.moveUp();
            break;
        case DOWN:
            a.moveDown();
            break;
        case LEFT:
            a.moveLeft(selected);
            break;
        case RIGHT:
            a.moveRight(selected);
            break;
        case BACKSPACE:
            a.delete_element(selected);
            break;
        case SPACE:
            a.insert_element();
            break;
        case W:
            app.setState({insertDir: 'Up'}, a.insert_element);
            break;
        case S:
            app.setState({insertDir: 'Down'}, a.insert_element);
            break;
        case D:
            app.setState({insertDir: 'Right'}, a.insert_element);
            break;
        case A:
            app.setState({insertDir: 'Left'}, a.insert_element);
            break;
        case T:
            a.secondSelect();
            break;
        case M:
            a.move();
            break;
        case E:
            a.extract();
            break;
        case Z:
            if (held_down.has(SHIFT)) 
                a.redo();
            else
                a.undo();
            break;
        case C:
            if (app.state.toConnect)
                a.connect();
            else 
                a.setToConnect();
            break;
        case ENTER:
            if (held_down.has(SHIFT)) 
                a.prevLine();
            else
                a.nextLine();
            break;
    }
}

export function setApp(_app){
    app = _app; 
}