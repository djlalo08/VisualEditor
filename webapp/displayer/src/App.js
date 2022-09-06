import { Xwrapper } from 'react-xarrows';
import './App.css';
import Horizontal from './Components/Horizontal';
import Map from './Components/Map';
import Vertical from './Components/Vertical';
import Wire from './Components/Wire';

function App() {
  return (
    <div className="App"> <Xwrapper>
      <Vertical>
        <Map className="io" name="ls" outs={[<div id="5"/>]} />
        <Map name="Min-Max"
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
                <Map name="test"/>,
                <div id="3"/>
              ]}
            />,
            <Map className="constant" name="2"/>
          ]} 
          outs={[
            <div id="4"/>
          ]} />
        <Horizontal>
          <Map className="io" name="min" ins={[<div id="6"/>]} />
          <Map className="io" name="avg" ins={[<div id="7"/>]} />
          <Map className="io" name="max" ins={[<div id="8"/>]} />
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