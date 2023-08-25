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
import { runTests } from './Utils/Tests';

// import GeneratedApp from './Components/GeneratedApp';
// import ExpectedApp from './Components/ExpectedApp';

/*
WORKING ON:
-Need to decide on what and how vertical returns. This calls for thinking about IR and homoiconicity again...

First: Go through all existing IRs and make sure they work and have tests
  -Fib isn't working. I think it's to do with having a recursive call with same inBound (a) twice. Gets confused with current val of a.

General goal: Try to get working quicksort, and fix any issues along the way
Specifically: Make filter work. There are issues with connecting wires.

InBinding and OutBinding, can be deleted and don't need to exist. We can just use nodes and check for the setvalue/getvalue attrs

Elements' unique IDs are line number in IR. Since there can only be 1 element per line, we know id is unique


THINK ABOUT:
-Have to reconcile horizontals with homiconic repr
-Maybe we do need nodes after all: 1) consider homoiconicity. 2) Say You want to select, or delete, or replace entire contents of a Node, You need to be able to select the Node, which means Node needs to exist
-Code has race conditions? See runTest having to call sleep() for more info

UP NEXT:
-Let's make quicksort!

-Put homoiconicity to work -- make a (I,O) be able to be treated as a function


TODOs: 
-Logic for whether stuff or isn't in lists when evaluating is sort of confusing and maybe wrong
-Add more imported knowledge when maps are added (variable arg count, nfix, recursive, inline, etc)
-Use window.showDirectoryPicker() to enable opening and saving files more directly
-Make maps for control flow:
  -For each
-Constants should have output nodes (and thus outBindings) [by default we can do hide_outs, returnidx:0]
-Test suite
-Update readme
-Add set/get maps to be used as variables
-Add left_out, right_out inserts
-Adding a constant assumes it is a number. Make flexible for other constant types
-Left/Right navigation in out nodes seems to not really work

VISUAL/AESTHETIC:
-Make if look better (condition on top, then/else side-by-side)
-If doesn't highlight when selected 


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
-What does unwrap attr in constants mean?

APPARENT INCONSISTENCIES:
-It seems that in some places InBound is characterized by getvalue, and in other cases by bind_idx. In yet other cases by name?

BUGS:
- When a map has more than 1 output, and it is called twice, the second time it's called it will add the output value as an attribute
*/
  


let id = 0;
// const FILE = 'inc';
// const FILE = 'inc_test';
// const FILE = 'lambda_nest';
// const FILE = 'lambdas';
// const FILE = 'if_test';
// const FILE = '2_arg_lambda';
// const FILE = '!';
// const FILE = '!_runner';
// const FILE = 'import_chain_test';
// const FILE = 'simple';
// const FILE = 'filter_test';
// const FILE = 'variable_test';
// const FILE = 'vertical_test';
// const FILE = 'quicksort';
// const FILE = 'quicksort_test';
// const FILE = 'cacheing_test';
// const FILE = 'x';
// const FILE = 'fib';
// const FILE = 'fib_runner';
// const FILE = 'ls';

// const FILE = 'empty';

const FILE = 'test';

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
  
  eval_(assertFn){
    let outbindings = updateOutbindings(this.state.AST);
    let eval_result = evaluate(this.state.selected, outbindings, this.state.imports);

    if (assertFn) {
      assertFn(eval_result);
    } else {
      console.log('eval result:');
      console.log(eval_result);
    }
    
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
      let [in_num, out_num] = countBounds(AST);
      irs[fileName.slice(0,-3)] = {
        import_from:'./irs/',
        in_num, out_num
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

    let {showModal, modalText, selected} = this.state;
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
        <Button onClick={() => runTests(this)}>Run Tests</Button>
        <p>Result: {eval_result}</p>
        <p>Selected Id: {selected ? selected.id : null}</p>
        {modal}
        <Sidebar node={this.state.selected} AST={AST}/>
      </div>
    );
  }
}


export default App;