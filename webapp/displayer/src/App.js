import React from 'react';
import FormControl from 'react-bootstrap/FormControl';
import Modal from 'react-bootstrap/Modal';
import { handleClose, setApp as setActions } from './Actions';
import './App.css';
import { ex } from './ir';
import { keypress, setApp as setKeyboard } from './KeyboardController';
import { ast_to_jsx } from './Utils/Converter';
import { parse } from './Utils/IrToAst';
import { printAst } from './Utils/NodeUtils';

// import GeneratedApp from './Components/GeneratedApp';
// import ExpectedApp from './Components/ExpectedApp';

class App extends React.Component{
  constructor(props){
    super(props);
    setActions(this);
    setKeyboard(this);
    
    this.handleTextChange = this.handleTextChange.bind(this);

    let AST = parse(ex);
    let [JSX, selected] = ast_to_jsx(AST);
    this.state = { AST, JSX, selected, 
      showModal: false,
      modalText: ''
    };
  }
  
  componentDidMount(){
    document.addEventListener("keydown", keypress);
  }

  componentWillUnmount(){
    document.removeEventListener("keydown", keypress);
  }
  
  handleTextChange(e){
    this.setState({modalText: e.target.value});
  }

  render(){
    return (
      <div className="App"> 
        <div>
          { this.state.JSX }
        </div>
        <button onClick={() => console.log(printAst(this.state.AST))}>Print AST</button> 
        <Modal show={this.state.showModal} onHide={handleClose}>
          <Modal.Body>
            <FormControl
              onChange={this.handleTextChange}
              value={this.state.modalText}
              autoFocus={true}
              type="text"
            /> 
          </Modal.Body>
        </Modal>
      </div>
    );
  }
}


export default App;