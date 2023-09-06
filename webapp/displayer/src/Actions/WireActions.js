import { app, updateAST } from '../Actions';
import { addAttr, delAttr, getAttrs, getName } from '../Utils/NodeUtils';


export function setToConnect() {
    let { selected } = app.state;

    if (getName(selected) != 'Node')
        return;

    addAttr(selected, 'to_connect', 't');
    app.setState({ toConnect: selected });

    updateAST();
}

export function connect() {
    let { selected, toConnect } = app.state;

    if (getName(selected) != 'Node')
        return;

    let start, end;
    if (getName(selected.parent) == 'Ins' &&
        getName(toConnect.parent) == 'Outs') {
        start = toConnect;
        end = selected;
    }
    else if (getName(selected.parent) == 'Outs' &&
        getName(toConnect.parent) == 'Ins') {
        end = toConnect;
        start = selected;
    }
    else {
        console.log('Invalid node pair for connection was selected');
    }

    let startAttrs = getAttrs(start);
    let value = startAttrs.setvalue || startAttrs.id * 100 || start.id;

    addAttr(start, 'setvalue', value);
    addAttr(end, 'getvalue', value);

    delAttr(toConnect, 'to_connect', 't');
    app.setState({ toConnect: null });

    updateAST();
}
