import { delete_element, setApp, updateSelected } from './Actions';
import './App.css';
import { ex } from './ir';
import { ast_to_jsx } from './Utils/Converter';
import { parse } from './Utils/IrToAst';
import { printAst } from './Utils/NodeUtils';

// import GeneratedApp from './Components/GeneratedApp';
// import ExpectedApp from './Components/ExpectedApp';
import React from "react";

const UP = 38;
const DOWN = 40;
const LEFT = 37;
const RIGHT = 39;
const BACKSPACE = 8;

class App extends React.Component{
  constructor(props){
    super(props);
    this.keypress = this.keypress.bind(this);
    setApp(this);
    
    let AST = parse(ex);
    let [JSX, selected] = ast_to_jsx(AST);
    this.state = { AST, JSX, selected};
  }
  
  keypress(e) {
    // console.log(e.keyCode);
    if (!this.state.selected) return;

    let {parent, children, idx} = this.state.selected;
    switch (e.keyCode) {
      case UP:
        updateSelected(parent);
        break;
      case DOWN:
        if (children) 
          updateSelected(children[0]);
        break;
      case LEFT:
        if (parent && idx > 0) 
          updateSelected(parent.children[idx-1]);
        break;
      case RIGHT:
        if (parent && idx < parent.children.length) 
          updateSelected(parent.children[idx+1]);
        break;
      case BACKSPACE:
        delete_element(this.state.selected);
    }
  }
  
  componentDidMount(){
    document.addEventListener("keydown", this.keypress);
  }

  componentWillUnmount(){
    document.removeEventListener("keydown", this.keypress);
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