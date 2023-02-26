import { setApp as setActions } from './Actions';
import './App.css';
import { ex } from './ir';
import { ast_to_jsx } from './Utils/Converter';
import { parse } from './Utils/IrToAst';
import { printAst } from './Utils/NodeUtils';

// import GeneratedApp from './Components/GeneratedApp';
// import ExpectedApp from './Components/ExpectedApp';
import React from "react";
import { keypress, setApp as setKeyboard } from './KeyboardController';

class App extends React.Component{
  constructor(props){
    super(props);
    setActions(this);
    setKeyboard(this);
    
    let AST = parse(ex);
    let [JSX, selected] = ast_to_jsx(AST);
    this.state = { AST, JSX, selected};
  }
  
  componentDidMount(){
    document.addEventListener("keydown", keypress);
  }

  componentWillUnmount(){
    document.removeEventListener("keydown", keypress);
  }
  
  shouldComponentUpdate(_, nextState){
    return this.state.AST != nextState.AST;
  }

  render(){
    return (
      <div className="App"> 
        <div>
          { this.state.JSX }
        </div>
        <button onClick={() => console.log(printAst(this.state.AST))}>Print AST</button> 
      </div>
    );
  }
}


export default App;