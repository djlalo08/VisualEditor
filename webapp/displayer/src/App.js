import React from 'react';
import Button from 'react-bootstrap/Button';
import FormControl from 'react-bootstrap/FormControl';
import Modal from 'react-bootstrap/Modal';
import { handleClose, openFile, setApp as setActions } from './Actions';
import './App.css';
import { Sidebar } from './Components/Sidebar';
import { keypress, keyrelease, setApp as setKeyboard } from './KeyboardController';
import { ast_to_jsx, loadImports } from './Utils/Converter';
import { evaluate, updateOutbindings } from './Utils/Evaluator';
import { parse } from './Utils/IrToAst';
import { addAttr, forEach, getImports, getInBounds, getOutBounds, printAst, updateInBindings } from './Utils/NodeUtils';

// import GeneratedApp from './Components/GeneratedApp';
// import ExpectedApp from './Components/ExpectedApp';

/*
  * 
Working on:
-Added sidebar. Begin to make it functional
-Clean up UI, and make it possible to write code in UI!

TODOs: 
-Make maps for control flow:
  -For each
-Test suite
-Update readme
-Add set/get maps to be used as variables
-Now that we can freely make stuff, try writing up some code in PO


IMPROVENTS/OPTIMIZATIONS IVE IGNORED:
-Hashing doesn't work on recursive fn calls
-Shouldn't be rerendering _everything_ every time

BUGS:
-
*/
  


let id = 0;
// const FILE = 'inc_test';
// const FILE = 'lambda_nest';
// const FILE = 'inc';
// const FILE = 'if_test';
// const FILE = 'lambdas';
// const FILE = '2_arg_lambda';
// const FILE = 'fib';
// const FILE = 'fib_runner';
// const FILE = '!';
// const FILE = 'x';
// const FILE = 'import_chain_test';
const FILE = 'simple';
// const FILE = 'cacheing_test';
// const FILE = 'test';
// const FILE = 'empty';

export function nextId(){
  return ++id;
}

export function resetIds(){
  id = 0;
}


class App extends React.Component{
  constructor(props){
    super(props);
    setActions(this);
    setKeyboard(this);
    
    this.handleTextChange = this.handleTextChange.bind(this);
    this.stateFromIR = this.stateFromIR.bind(this);
    this.eval_ = this.eval_.bind(this);
    this.addImport = this.addImport.bind(this);

    this.state = {
      imports: {},
      ...this.emptyState()
    }
    
  }
  
  eval_(){
    let outbindings = updateOutbindings(this.state.AST);
    let eval_result = evaluate(this.state.selected, outbindings, this.state.imports);
    console.log('eval result:');
    console.log(eval_result);
    if (typeof eval_result === 'function')
      eval_result += ' ';
    this.setState({eval_result});
  }
  
  emptyState(){
    return { 
      AST: null,
      JSX: null,
      selected: null, 
      showModal: false,
      modalText: '',
      secondSelect: null,
      lastIRs: [],
      nextIRs: [],
      insertDir: '',
      toConnect: null,
      eval_result: null,
    };
  }
  
  stateFromIR(fileText){
    let AST = parse(fileText);
    let [JSX, selected] = ast_to_jsx(AST);
    return {
      ...this.emptyState(),
      AST, JSX, selected,
    } 
  }
  
  addImport(importName, importIR){
    if (!this || !this.state)
      return;

    if (importName in this.state.imports)
      return;

    let AST = parse(importIR);
    
    let importsList = new Set(getImports(AST));
    if (importsList.has(importName)){
      forEach(AST, node => addAttr(node, 'dontCache', 't'))  
    }

    loadImports(AST);
    let outbindings = updateOutbindings(AST);
    let outBounds = getOutBounds(AST);
    let inBounds = getInBounds(AST);

    let imports = {...this.state.imports};
    let fn = (bindings, externalMaps) => {
      updateInBindings(inBounds, bindings);
      return outBounds.map(ob => evaluate(ob, outbindings, externalMaps));
    }

    imports[importName] = fn;
    this.setState({imports});
  }

  componentDidMount(){
    document.addEventListener("keydown", keypress);
    document.addEventListener("keyup", keyrelease);
    openFile(FILE);
  }

  componentWillUnmount(){
    document.removeEventListener("keydown", keypress);
    document.removeEventListener("keyup", keyrelease);
  }
  
  handleTextChange(e){
    this.setState({modalText: e.target.value});
  }
  
  
  download(filename, text){
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);
  
    element.style.display = 'none';
    document.body.appendChild(element);
  
    element.click();
  
    document.body.removeChild(element);
  }

  render(){
    let {eval_result, AST, JSX} = this.state;
    if (eval_result && eval_result.join){
      eval_result = eval_result.join(', ');
    }

    let {showModal, modalText} = this.state;
    let modal = <Modal show={showModal} onHide={handleClose}>
      <Modal.Body>
        <FormControl
          onChange={this.handleTextChange}
          value={modalText}
          autoFocus={true}
          type="text"
        /> 
      </Modal.Body>
    </Modal>

    return (
      <div className="App"> 
        <h1>{FILE}.ir</h1>
        <div>
          { JSX }
        </div>
        <Button onClick={() => console.log(printAst(AST))}>Print AST</Button> 
        <Button onClick={() => openFile(FILE)}>Load ex1</Button>
        <Button onClick={() => this.download('file.ir', printAst(AST))}>Save</Button>
        <Button onClick={() => this.eval_()}>Eval</Button>
        <p>{eval_result}</p>
        {modal}
        <Sidebar node={this.state.selected}/>
      </div>
    );
  }
}


export default App;