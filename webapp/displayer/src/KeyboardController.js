import { delete_element, updateSelected } from "./Actions";

const UP = 38;
const DOWN = 40;
const LEFT = 37;
const RIGHT = 39;
const BACKSPACE = 8;

let app = null;

export function keypress(e){
    // console.log(e.keyCode);
    if (!app.state.selected) return;

    let {parent, children, idx} = app.state.selected;
    switch (e.keyCode) {
      case UP:
        updateSelected(parent);
        break;
      case DOWN:
        if (children && children.length) 
          updateSelected(children[0]);
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
        delete_element(app.state.selected);
    }
}

export function setApp(_app){
    app = _app; 
}