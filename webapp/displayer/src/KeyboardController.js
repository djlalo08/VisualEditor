import * as a from "./Actions";

const UP = 38;
const DOWN = 40;
const LEFT = 37;
const RIGHT = 39;
const BACKSPACE = 8;
const SPACE = 32;
const ENTER = 13;
const SHIFT = 16;
const COMMAND_L = 91;
const COMMAND_R = 93;

const PLUS = 187;
const MINUS = 189;

const A = 65;
const C = 67;
const D = 68;
const E = 69;
const I = 73;
const M = 77;
const O = 79;
const S = 83;
const T = 84;
const W = 87;
const Z = 90;

let app = null;
let held_down = new Set();

export function keyrelease(e){
    held_down.delete(e.keyCode);
}

export function keypress(e){
    // console.log(e.keyCode);
    held_down.add(e.keyCode);

    let {selected, showModal, modalAction} = app.state;

    if (showModal) {
        if (e.keyCode == ENTER){
            modalAction();
        }
        return;
    }
    
    if (!selected) return;

    let shift = held_down.has(SHIFT);
    let command = held_down.has(COMMAND_L) || held_down.has(COMMAND_R);
    let i_key = held_down.has(I);
    let o_key = held_down.has(O);

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
        app.setState({modalAction: a.insertMapFromModal, insertDir: shift? 'Wrap' : 'In'}, a.insert_element);
        break;
    case W:
        app.setState({modalAction: a.insertMapFromModal, insertDir: 'Up'}, a.insert_element);
        break;
    case S:
        app.setState({modalAction: a.insertMapFromModal, insertDir: 'Down'}, a.insert_element);
        break;
    case D:
        app.setState({modalAction: a.insertMapFromModal, insertDir: shift? 'Right_Out' : 'Right_In'}, a.insert_element);
        break;
    case A:
        app.setState({modalAction: a.insertMapFromModal, insertDir: shift? 'Left_Out' : 'Left_In'}, a.insert_element);
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
        if (shift)
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
        if (shift)
            a.prevLine();
        else if (command)
            a.callEval();
        else
            a.nextLine();
        break;
    case PLUS:
        if (i_key){
            a.incMapIns(selected);
        } else if (o_key){
            //Can we really ever modify out count?
        }
        break;
    case MINUS:
        if (i_key){
            a.decMapIns(selected);
        } else if (o_key){
            //Can we ever really modify outcount?
        }
    }
}

export function setApp(_app){
    app = _app; 
}