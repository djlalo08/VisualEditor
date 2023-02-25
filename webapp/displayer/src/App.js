import './App.css';
import GeneratedApp from './Components/GeneratedApp';
import { ex } from './ir';
import { ast_to_jsx } from './Utils/Converter';
import { parse } from './Utils/IrToAst';
// import GeneratedApp from './Components/GeneratedApp';
// import ExpectedApp from './Components/ExpectedApp';
import $ from 'jquery';
import React from "react";


class App extends React.Component{
  constructor(props){
    super(props);
    this.fetchAndLog = this.fetchAndLog.bind(this);
    this.state = { AST: parse(ex), selected: null};
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
          { ast_to_jsx(this.state.AST) } 
        </div>
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