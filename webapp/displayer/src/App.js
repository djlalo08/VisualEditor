import './App.css';
import GeneratedApp from './Components/GeneratedApp';
import { ex } from './ir';
import { ast_to_jsx } from './Utils/Converter';
import { parse } from './Utils/IrToAst';
import { addAttr, delAttr, printAst } from './Utils/NodeUtils';
// import GeneratedApp from './Components/GeneratedApp';
// import ExpectedApp from './Components/ExpectedApp';
import $ from 'jquery';
import React from "react";


class App extends React.Component{
  constructor(props){
    super(props);
    this.fetchAndLog = this.fetchAndLog.bind(this);
    this.updateSelected = this.updateSelected.bind(this);
    this.updateAST = this.updateAST.bind(this);
    
    let AST = parse(ex);
    let [JSX, selected] = ast_to_jsx(AST, this.updateSelected);
    this.state = { AST, JSX, selected};
  }
  
  updateSelected(new_selection){
    let {selected} = this.state;
    if (selected) 
      delAttr(selected, 'selected');

    if (selected == new_selection)
        this.setState({selected: null});

    else {
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
        <GeneratedApp/> 
        <br/>
        <button onClick={this.fetchAndLog(`http://localhost:5000/clear`)}>Clear</button> 
        <button onClick={this.fetchAndLog(`http://localhost:5000/show/id_map`)}>Show map</button> 
        <button onClick={this.fetchAndLog(`http://localhost:5000/show/ir`)}>Show ir</button> 
        <button onClick={this.fetchAndLog(`http://localhost:5000/show/inited`)}>Show inited</button> 
        <button onClick={this.fetchAndLog(`http://localhost:5000/show/all`)}>Show all</button> 
        <div>
          { this.state.JSX }
        </div>
        <button onClick={() => console.log(printAst(this.state.AST))}>Print AST</button> 
      </div>
    );
  }

  fetchAndLog(url){
    return async () => {
      $.ajax(url, 
        {xhrFields: {withCredentials: true}, 
        success: text => console.log(text), 
        crossDomain: true});
    }
  }
}


export default App;