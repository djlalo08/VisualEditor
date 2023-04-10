import React from 'react';
import Button from 'react-bootstrap/Button';
import FormControl from 'react-bootstrap/FormControl';
import Modal from 'react-bootstrap/Modal';
import { handleClose, openFile, setApp as setActions } from './Actions';
import './App.css';
import { ex } from './ir';
import { keypress, keyrelease, setApp as setKeyboard } from './KeyboardController';
import { ast_to_jsx } from './Utils/Converter';
import { eval_ as e, updateOutbindings } from './Utils/Evaluator';
import { parse } from './Utils/IrToAst';
import { printAst } from './Utils/NodeUtils';

// import GeneratedApp from './Components/GeneratedApp';
// import ExpectedApp from './Components/ExpectedApp';

/*
TODOs: 
-Make maps for control flow:
  -For each
  -Map
  -Filter
-Add saving
-Add ability to pull up actual existing nodes
-Add set/get maps to be used as variables
-Now that we can freely make stuff, try writing up some code in PO
*/
let id = 0;
const FILE = 'ls';

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

    this.state = this.stateFromIR(ex);
  }
  
  eval_(){
    updateOutbindings(this.state.AST);
    let eval_result = e(this.state.selected);
    this.setState({eval_result});
  }
  
  stateFromIR(fileText){
    let AST = parse(fileText);
    let [JSX, selected] = ast_to_jsx(AST);

    return { AST, JSX, selected, 
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
        <div>
          { JSX }
        </div>
        <Button onClick={() => console.log(printAst(AST))}>Print AST</Button> 
        <Button onClick={() => openFile(FILE)}>Load ex1</Button>
        <Button onClick={() => this.download('file.ir', printAst(AST))}>Save</Button>
        <Button onClick={() => this.eval_()}>Eval</Button>
        <p>{eval_result}</p>
        {modal}
      </div>
    );
  }
}


export default App;