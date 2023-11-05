import * as a from "./Actions";
import * as insert_element from './Actions/InsertionActions';
import * as moveUpToVertical from './Actions/NavigationActions';
import * as updateSelected from './Actions/SelectionActions';
import * as UNDO_LIMIT from './Actions/UndoActions';
import * as setToConnect from './Actions/WireActions';

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
        moveUpToVertical.moveUp();
        break;
    case DOWN:
        moveUpToVertical.moveDown();
        break;
    case LEFT:
        moveUpToVertical.moveLeft(selected);
        break;
    case RIGHT:
        moveUpToVertical.moveRight(selected);
        break;
    case BACKSPACE:
        insert_element.delete_element(selected);
        break;
    case SPACE:
        app.setState({modalAction: insert_element.insertMapFromModal, insertDir: shift? 'Wrap' : 'In'}, insert_element.insert_element);
        break;
    case W:
        app.setState({modalAction: insert_element.insertMapFromModal, insertDir: 'Up'}, insert_element.insert_element);
        break;
    case S:
        app.setState({modalAction: insert_element.insertMapFromModal, insertDir: 'Down'}, insert_element.insert_element);
        break;
    case D:
        app.setState({modalAction: insert_element.insertMapFromModal, insertDir: shift? 'Right_Out' : 'Right_In'}, insert_element.insert_element);
        break;
    case A:
        app.setState({modalAction: insert_element.insertMapFromModal, insertDir: shift? 'Left_Out' : 'Left_In'}, insert_element.insert_element);
        break;
    case T:
        updateSelected.secondSelect();
        break;
    case M:
        insert_element.move();
        break;
    case E:
        insert_element.extract();
        break;
    case Z:
        if (shift)
            UNDO_LIMIT.redo();
        else
            UNDO_LIMIT.undo();
        break;
    case C:
        if (app.state.toConnect)
            setToConnect.connect();
        else 
            setToConnect.setToConnect();
        break;
    case ENTER:
        if (shift)
            moveUpToVertical.prevLine();
        else if (command)
            a.callEval();
        else
            moveUpToVertical.nextLine();
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
        break;
    case I:
        if (command){
            a.toggleInLine(selected);
        }
        break;
    }
}

export function setApp(_app){
    app = _app; 
}