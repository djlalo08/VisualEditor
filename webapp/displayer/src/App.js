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
import { addAttr, countBounds, forEach, getImports, getInBounds, getOutBounds, printAst, updateInBindings } from './Utils/NodeUtils';

// import GeneratedApp from './Components/GeneratedApp';
// import ExpectedApp from './Components/ExpectedApp';

/*
WORKING ON:
-Clean up UI, and make it possible to write code in UI!
    -A and D behavior is a bit weird
    -Navigation is wonky


UP NEXT:
-Let's make quicksort!

-Put homoiconicity to work -- make a (I,O) be able to be treated as a function


TODOs: 
-Add more imported knowledge when maps are added (variable arg count, nfix, recursive, inline, etc)
-Make maps from mapRepo import necessary knowledge (insCount, outsCount, nfix, inline, etc)
-Make maps for control flow:
  -For each
-Test suite
-Update readme
-Add set/get maps to be used as variables
-Now that we can freely make stuff, try writing up some code in PO

VISUAL/AESTHETIC:
-Make if look better (condition on top, then/else side-by-side


IMPROVENTS/OPTIMIZATIONS IVE IGNORED:
-Hashing doesn't work on recursive fn calls
-Data unpacking (output node can return components of a result obj, rather than the obj itself, if user wants)
-Shouldn't be rerendering _everything_ every time

INTERESTING IDEAS:
- IR Representation need not be in text to be parsed. This might make representation easier (of course, repr should still be one-to-one with a text version). Now that I'm back, I like textual IR again. Could be possible to compress it, but not necessary atm. Parsing is relatively trivial and already take care of -- not a major issue

Q and A:
-What is the difference between In/OutBinding and In/OutBound? 
  Binding is for wire connections
  Bound is for params (i.e. InBound are function arguments, OutBound are for function returns)

APPARENT INCONSISTENCIES:
-It seems that in some places InBound is characterized by getvalue, and in other cases by bind_idx. In yet other cases by name?

BUGS:
-
*/
  


let id = 0;
// const FILE = 'inc_test';
// const FILE = 'lambda_nest';
// const FILE = 'inc';
// const FILE = 'if_test';
const FILE = 'lambdas';
// const FILE = '2_arg_lambda';
// const FILE = 'fib';
// const FILE = 'fib_runner';
// const FILE = '!';
// const FILE = 'x';
// const FILE = 'import_chain_test';
// const FILE = 'simple';
// const FILE = 'cacheing_test';
// const FILE = 'test';
// const FILE = 'empty';
// const FILE = 'ls';

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
    this.onShow = this.onShow.bind(this);
    this.stateFromIR = this.stateFromIR.bind(this);
    this.eval_ = this.eval_.bind(this);
    this.addImport = this.addImport.bind(this);
    this.getIRsList = this.getIRsList.bind(this);

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
      irDirHandle: null,
      irs: {},
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
    
    let importsMap = getImports(AST);
    let isRecursive = importsMap.hasOwnProperty(importName);
    if (isRecursive){
      forEach(AST, node => addAttr(node, 'dont_cache', 't'))  
    }

    loadImports(AST);
    let outbindings = updateOutbindings(AST);
    let outBounds = getOutBounds(AST);
    let inBounds = getInBounds(AST);

    let fn = (bindings, externalMaps) => {
      updateInBindings(inBounds, bindings);
      return outBounds.map(ob => evaluate(ob, outbindings, externalMaps));
    }

    let imports = {...this.state.imports};
    imports[importName] = fn;
    this.setState({imports});
  }

  componentDidMount(){
    document.addEventListener("keydown", keypress);
    document.addEventListener("keyup", keyrelease);
    openFile(FILE);
  }

  async getIRsList(){
    let handle = this.state.irDirHandle || await window.showDirectoryPicker();
    let irs = {};
    for await (const [fileName, fileHandle] of handle.entries()){
      let file = await fileHandle.getFile();
      let fileText = await file.text();
      let AST = parse(fileText);
      let [inCount, outCount] = countBounds(AST);
      irs[fileName.slice(0,-3)] = {
        import_from:'./irs/',
        inCount, outCount
      };
    }

    this.setState({irs, irDirHandle: handle});
  }

  componentWillUnmount(){
    document.removeEventListener("keydown", keypress);
    document.removeEventListener("keyup", keyrelease);
  }
  
  handleTextChange(e){
    this.setState({modalText: e.target.value});
  }
  
  onShow(){
    setTimeout(() =>  this.setState({modalText: ''}), 10);
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
    let modal = <Modal show={showModal} onHide={handleClose} onShow={this.onShow}>
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
        <Button onClick={this.getIRsList}>FileStuff</Button>
        <p>{eval_result}</p>
        {modal}
        <Sidebar node={this.state.selected} AST={AST}/>
      </div>
    );
  }
}


export default App;