import { ast_to_jsx } from './Utils/Converter';
import { evaluate } from './Utils/Evaluator';
import { updateToMatchLength } from './Utils/ListUtils';
import { makeNode } from './Utils/NodeUtils';

export let app = null;

export function setApp(_app){
    app = _app;
}

export function updateAST(callback){
    let JSX = ast_to_jsx(app.state.AST)[0];
    app.setState({AST: {...app.state.AST}, JSX}, callback);
}

export function callEval(assertFn){
    let {selected, AST, import_irs} = app.state;
    let eval_result = evaluate(selected, [], AST, import_irs);

    if (assertFn) {
      assertFn(eval_result);
    } else {
      console.log('eval result:');
      console.log(eval_result);
    }
    
    if (typeof eval_result === 'function')
      eval_result += ' ';
    app.setState({eval_result});
  }


export function setMapIns(map, count){
    let [ins, _] = map.children;
    updateToMatchLength(count, ins.children, () => makeNode(ins));
    for (let i = 0; i < ins.children.length; i++){
        ins.children[i].idx = i;
    }
    updateAST();
}

export function incMapIns(map){
    let oldLength = map.children[0].children.length;
    setMapIns(map, oldLength+1);
}

export function decMapIns(map){
    let oldLength = map.children[0].children.length;
    setMapIns(map, oldLength-1);
}
