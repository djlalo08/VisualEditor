import './App.css';
import GeneratedApp from './Components/GeneratedApp';
import { run_parse } from './Utils/Converter';
// import GeneratedApp from './Components/GeneratedApp';
// import ExpectedApp from './Components/ExpectedApp';
import $ from 'jquery';


function App() {
  return (
    <div className="App"> 
      <GeneratedApp/> 
      <br/>
      <button onClick={fetchAndLog(`http://localhost:5000/clear`)}>Clear</button> 
      <button onClick={fetchAndLog(`http://localhost:5000/show/id_map`)}>Show map</button> 
      <button onClick={fetchAndLog(`http://localhost:5000/show/ir`)}>Show ir</button> 
      <button onClick={fetchAndLog(`http://localhost:5000/show/inited`)}>Show inited</button> 
      <button onClick={fetchAndLog(`http://localhost:5000/show/all`)}>Show all</button> 
      <button onClick={run_parse}>Parse</button> 
      <div>
        {run_parse()} 
      </div>
    </div>
  );
}

  function fetchAndLog(url){
    return async () => {
      $.ajax(url, 
        {xhrFields: {withCredentials: true}, 
        success: text => console.log(text), 
        crossDomain: true});
    }
  }

export default App;