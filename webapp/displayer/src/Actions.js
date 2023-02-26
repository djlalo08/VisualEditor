import { ast_to_jsx } from './Utils/Converter';
import { addAttr, delAttr, getName } from './Utils/NodeUtils';

let app = null;

export function setApp(_app){
    app = _app;
}

export function updateSelected(new_selection){
    let {selected} = app.state;
    if (selected) 
        delAttr(selected, 'selected');

    if (selected == new_selection)
        app.setState({selected: null});

    else {
        if (new_selection)
            addAttr(new_selection, 'selected', 't');
        app.setState({selected: new_selection});
    }

    updateAST();
}

export function delete_element(elmt_to_del){
    if (!elmt_to_del)
        return;

    let {parent, idx} = elmt_to_del;

    switch (getName(elmt_to_del)){
        case 'Map':
            parent.children.splice(idx, 1);
            break;
        case 'Node':
            elmt_to_del.children = [];
            break;        
        default:
            return;
    }
    
    updateAST();
}
  
export function updateAST(){
    let JSX = ast_to_jsx(app.state.AST, app.updateSelected)[0];
    app.setState({AST: {...app.state.AST}, JSX});
}