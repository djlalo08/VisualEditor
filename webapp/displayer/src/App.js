import React from 'react';
import Button from 'react-bootstrap/Button';
import FormControl from 'react-bootstrap/FormControl';
import Modal from 'react-bootstrap/Modal';
import { handleClose, setApp as setActions } from './Actions';
import './App.css';
import { ex } from './ir';
import { keypress, keyrelease, setApp as setKeyboard } from './KeyboardController';
import { ast_to_jsx } from './Utils/Converter';
import { parse } from './Utils/IrToAst';
import { printAst } from './Utils/NodeUtils';

// import GeneratedApp from './Components/GeneratedApp';
// import ExpectedApp from './Components/ExpectedApp';

/*
TODOs: 
-Maybe go back to compiler side
-Add saving
-Add ability to pull up actual existing nodes
-Add set/get maps to be used as variables
-Now that we can freely make stuff, try writing up some code in PO
*/
let id = 0;

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
    this.openFile = this.openFile.bind(this);

    this.state = this.stateFromIR(ex);
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
      toConnect: null
    };
  }

  componentDidMount(){
    document.addEventListener("keydown", keypress);
    document.addEventListener("keyup", keyrelease);
  }

  componentWillUnmount(){
    document.removeEventListener("keydown", keypress);
    document.removeEventListener("keyup", keyrelease);
  }
  
  handleTextChange(e){
    this.setState({modalText: e.target.value});
  }
  
  openFile(){
    let _this = this;
    fetch('./irs/ex1.ir')
    .then(response => response.text())
    .then(text => _this.setState(_this.stateFromIR(text)));
  }

  render(){
    let modal = <Modal show={this.state.showModal} onHide={handleClose}>
      <Modal.Body>
        <FormControl
          onChange={this.handleTextChange}
          value={this.state.modalText}
          autoFocus={true}
          type="text"
        /> 
      </Modal.Body>
    </Modal>

    return (
      <div className="App"> 
        <div>
          { this.state.JSX }
        </div>
        <Button onClick={() => console.log(printAst(this.state.AST))}>Print AST</Button> 
        <Button onClick={this.openFile}>Load ex1</Button>
        {modal}
      </div>
    );
  }
}


export default App;