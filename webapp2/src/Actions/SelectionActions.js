import { app, updateAST } from '../Actions';
import { addAttr, delAttr, getName } from '../Utils/NodeUtils';


export function updateSelected(new_selection, callback) {
    let { selected } = app.state;
    if (selected)
        delAttr(selected, 'selected');

    if (selected == new_selection)
        app.setState({ selected: null });

    else {
        if (new_selection)
            addAttr(new_selection, 'selected', 't');
        app.setState({ selected: new_selection });
    }

    updateAST(callback);
}

export function setSelectedById(id, callback) {
    updateSelected(findNodeWithId(id, app.state.AST), callback);
}
function findNodeWithId(id, node) {
    let cur_id = node.id;
    if (cur_id == id)
        return node;

    for (let child of node.children) {
        let result = findNodeWithId(id, child);
        if (result)
            return result;
    }

    return null;
}

export function secondSelect() {
    let { selected, secondSelect } = app.state;

    if (!selected)
        return;

    if (getName(selected) != 'Map')
        return;

    if (secondSelect) {
        delAttr(secondSelect, 'second_select');
    }

    addAttr(selected, 'second_select', 't');
    app.setState({ secondSelect: selected });

    updateAST();
}
