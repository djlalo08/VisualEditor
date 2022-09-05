import { Xwrapper } from 'react-xarrows';
import './App.css';
import Horizontal from './Horizontal';
import Map from './Map.js';
import Vertical from './Vertical.js';
import Wire from './Wire';

function App() {
  return (
    <div className="App"> <Xwrapper>
      <Vertical>
        <Map className="io" name="ls" outs={[<div id="5"/>]} />
        <Map name="min-max"
          ins={[
            <div id="9"/>
          ]} 
          outs={[
            <div id="0"/>,
            <div id="1"/>
          ]}
        /> 
        <Map name="/"
          ins={[
            <Map name="+"
              ins={[
                <div id="2"/>,
                <div id="3"/>
              ]}
            />,
            <Map name="2"/>
          ]} 
          outs={[
            <div id="4"/>
          ]} />
        <Horizontal>
          <Map className="io" name="min" outs={[<div id="6"/>]} />
          <Map className="io" name="avg" outs={[<div id="7"/>]} />
          <Map className="io" name="max" outs={[<div id="8"/>]} />
        </Horizontal>
      </Vertical>
      <Wire start="0" end="2"/>
      <Wire start="1" end="3"/>
      <Wire start="5" end="9"/>
      <Wire start="0" end="6"/>
      <Wire start="4" end="7"/>
      <Wire start="1" end="8"/>

    </Xwrapper> </div>
  );
}

export default App;