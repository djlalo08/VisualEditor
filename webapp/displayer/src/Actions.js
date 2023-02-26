import { ast_to_jsx } from './Utils/Converter';
import { addAttr, delAttr } from './Utils/NodeUtils';

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
            addAttr(new_selection, 'selected', 'true');
        app.setState({selected: new_selection});
    }

    updateAST();
}
  
export function updateAST(){
    let JSX = ast_to_jsx(app.state.AST, app.updateSelected)[0];
    app.setState({AST: {...app.state.AST}, JSX});
}