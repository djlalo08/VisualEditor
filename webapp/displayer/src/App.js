import './App.css';
import { ex } from './ir';
import { ast_to_jsx } from './Utils/Converter';
import { parse } from './Utils/IrToAst';
import { addAttr, delAttr, printAst } from './Utils/NodeUtils';
// import GeneratedApp from './Components/GeneratedApp';
// import ExpectedApp from './Components/ExpectedApp';
import React from "react";

const UP = 38;
const DOWN = 40;
const LEFT = 37;
const RIGHT = 39;

class App extends React.Component{
  constructor(props){
    super(props);
    this.updateSelected = this.updateSelected.bind(this);
    this.updateAST = this.updateAST.bind(this);
    this.keypress = this.keypress.bind(this);
    
    let AST = parse(ex);
    let [JSX, selected] = ast_to_jsx(AST, this.updateSelected);
    this.state = { AST, JSX, selected};
  }
  
  keypress(e) {
    if (!this.state.selected) return;

    let {parent, children, idx} = this.state.selected;
    switch (e.keyCode) {
      case UP:
        this.updateSelected(parent);
        break;
      case DOWN:
        if (children) 
          this.updateSelected(children[0]);
        break;
      case LEFT:
        if (parent && idx > 0) 
          this.updateSelected(parent.children[idx-1]);
        break;
      case RIGHT:
        if (parent && idx < parent.children.length) 
          this.updateSelected(parent.children[idx+1]);
        break;
    }
  }
  
  componentDidMount(){
    document.addEventListener("keydown", this.keypress);
  }

  componentWillUnmount(){
    document.removeEventListener("keydown", this.keypress);
  }
  
  updateSelected(new_selection){
    let {selected} = this.state;
    if (selected) 
      delAttr(selected, 'selected');

    if (selected == new_selection)
        this.setState({selected: null});

    else {
      if (new_selection)
        addAttr(new_selection, 'selected', 'true');
      this.setState({selected: new_selection});
    }
   
    this.updateAST();
  }
  
  updateAST(){
    let JSX = ast_to_jsx(this.state.AST, this.updateSelected)[0];
    this.setState({AST: {...this.state.AST}, JSX});
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