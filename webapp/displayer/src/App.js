import React from 'react';
import Button from 'react-bootstrap/Button';
import FormControl from 'react-bootstrap/FormControl';
import Modal from 'react-bootstrap/Modal';
import { callEval, setApp as setActions } from './Actions';
import { openFile } from './Actions/FileActions';
import { handleClose } from './Actions/ModalActions';
import './App.css';
import { Sidebar } from './Components/Sidebar';
import { keypress, keyrelease, setApp as setKeyboard } from './KeyboardController';
import { ast_to_jsx } from './Utils/Converter';
import { parse } from './Utils/IrToAst';
import { countBounds, printAst } from './Utils/NodeUtils';

let devMode = true;
let id = 0;
// const FILE = 'inc_test';
// const FILE = '2_outs';
// const FILE = '2_outs_test';
// const FILE = 'lambda_nest';
// const FILE = 'lambdas';
// const FILE = 'if_test';
// const FILE = '2_arg_lambda';
// const FILE = '!';
// const FILE = 'import_chain_test';
// const FILE = 'simple';
// const FILE = 'filter_test';
// const FILE = 'variable_test';
// const FILE = 'vertical_test';
// const FILE = 'quicksort';
// const FILE = 'quicksort_test';
// const FILE = 'fib';
// const FILE = 'fnsTest';
const FILE = 'fnsTestSimpl';
// const FILE = 'fn_ex';
// const FILE = 'if_test';
// const FILE = 'first_index';
// const FILE = 'azure_example';

// const FILE = 'x';
// const FILE = 'cacheing_test';

// const FILE = 'empty';
// const FILE = 'fns';
// const FILE = 'test';

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
    this.requestDirHandler = this.requestDirHandler.bind(this);
    this.getIRsList = this.getIRsList.bind(this);

    this.state = {
      ...this.emptyState()
    }
    
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
      modalAction: null,
      toConnect: null,
      eval_result: null,
      irDirHandle: null,
      irs: {},
      import_irs: {},
      activeFile: FILE,
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
  
  componentDidMount(){
    document.addEventListener("keydown", keypress);
    document.addEventListener("keyup", keyrelease);
    openFile(this.state.activeFile);
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

  requestDirHandler(){
    if (devMode) return;
    if (!this.state.irDirHandle){
      let r = window.showDirectoryPicker();
      this.setState({irDirHandle: r});
    }
  }

  render(){
    let {eval_result, AST, JSX} = this.state;
    if (eval_result && eval_result.join){
      eval_result = eval_result.join(', ');
    }

    let {showModal, modalText, selected, activeFile} = this.state;
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

    let fileButton = fileName => <Button className='button' onClick={() => openFile(fileName)}>{fileName}</Button>;

    let demoButtons = (<>
      {fileButton('basic')}
      {fileButton('discr')}
      {fileButton('fns')}
    </>);

    return (
      <div className="App" onMouseDown={this.requestDirHandler}> 
        <h1>{activeFile}.ir</h1>
        <div>
          { JSX }
        </div>
        <p>Result: {eval_result}</p>
        {/* <p>Selected Id: {selected ? selected.id : null}</p> */}
        <Button className='button' onClick={() => navigator.clipboard.writeText(printAst(AST))}>Copy AST</Button>
        <Button className='button' onClick={() => console.log(printAst(AST))}>Print AST</Button> 
        {/* <Button onClick={() => this.download('file.ir', printAst(AST))}>Save</Button> */}
        <Button className='button' onClick={callEval}>Eval</Button>
        {/* <Button onClick={this.getIRsList}>FileStuff</Button> */}
        {/* <Button onClick={() => runTests(this)}>Run Tests</Button> */}
        {/* <Button onClick={openFileFromDir}>Open</Button> */}
        {/* <Button onClick={save}>Save</Button> */}

        <br/>
        <br/>
        Demo Pages
        <br/>
        {demoButtons}

        
        {modal}
        <Sidebar node={this.state.selected} AST={AST}/>
      </div>
    );
  }
}

export default App;