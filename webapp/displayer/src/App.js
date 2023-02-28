import React from 'react';
import FormControl from 'react-bootstrap/FormControl';
import Modal from 'react-bootstrap/Modal';
import { Xwrapper } from 'react-xarrows';
import { handleClose, setApp as setActions } from './Actions';
import './App.css';
import { Constx } from './Components/Constx';
import { H } from './Components/H';
import { V } from './Components/V';
import Wire from './Components/Wire';
import { ex } from './ir';
import { keypress, keyrelease, setApp as setKeyboard } from './KeyboardController';
import { Mapx } from './Mapx';
import { Nodex } from './Nodex';
import { ast_to_jsx } from './Utils/Converter';
import { parse } from './Utils/IrToAst';

// import GeneratedApp from './Components/GeneratedApp';
// import ExpectedApp from './Components/ExpectedApp';


//TODO: Insert nodes to right and left, 
//TODO: insert node above, below
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
      modalText: '',
      secondSelect: null,
      lastIRs: [],
      nextIRs: [],
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
        {/* <Button onClick={() => console.log(printAst(this.state.AST))}>Print AST</Button>  */}
        {modal}
        <Xwrapper>
          <H>
          <Mapx name="sqrt">
            {[
              <Nodex>
                <Mapx name="-" infix>
                  {[
                    <Nodex>
                      <Mapx name="sqr">
                        {[
                          <Nodex></Nodex>,
                        ]}
                        {[ ]} 
                      </Mapx>
                    </Nodex>,
                    <Nodex>
                      <V>
                        <H>
                          <Mapx name="*" infix>
                            {[
                              <Nodex>
                                <Constx name='4'/> 
                              </Nodex>,
                              <Nodex>
                                
                              </Nodex>,
                              <Nodex>
                                
                              </Nodex>
                            ]}
                            {[
                              <Nodex id='1111'/>
                            ]}
                          </Mapx>
                          <V>
                            <Mapx name="Z">
                              {[]}
                              {[
                                <Nodex id='z'/>
                              ]}
                            </Mapx>
                            <Mapx name="ZZ">
                              {[]}
                              {[]}
                            </Mapx>
                          </V>
                        </H>
                        <Mapx name="W">
                          {[
                            <Nodex id='2222'/>,
                            <Nodex id='z2'/>,
                          ]}
                          {[]}
                        </Mapx>
                      </V>
                    </Nodex>
                  ]}
                  {[]}
                </Mapx>
              </Nodex>
            ]}
            {[
            ]}
          </Mapx>
          <V>
            <Constx name='X'/>
            <Constx name='Y'/>
          </V>
        </H>
        <Wire start='1111' end='2222'/>
        <Wire start='z' end='z2'/>
        </Xwrapper>
      </div>
    );
  }
}


export default App;