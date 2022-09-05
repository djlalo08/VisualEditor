import { Xwrapper } from 'react-xarrows';
import './App.css';
import Map from './Map.js';
import Node from './Node';
import Vertical from './Vertical.js';
import Wire from './Wire';

function App() {
  return (
    <div className="App"> <Xwrapper>
      <Vertical>
        <Map name="min-max"
          ins={[
            <Node/>
          ]} 
          outs={[
            <Node id="elem0"/>,
            <Node id="elem1"/>
          ]}
        /> 
        <Map name="/"
          ins={[
            <Map name="+"
              ins={[
                <Node id="elem2"/>,
                <Node id="elem3"/>
              ]}
            />,
            <Map name="2"/>
          ]} 
          outs={[
            <Node id="elem4"/>
          ]} />
      </Vertical>
      <Wire start="elem0" end="elem2"/>
      <Wire start="elem1" end="elem3"/>

    </Xwrapper> </div>
  );
}

export default App;