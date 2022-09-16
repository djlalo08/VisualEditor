import { Xwrapper } from 'react-xarrows';
import Horizontal from './Horizontal';
import Ins from './Ins';
import Map from './Map';
import Outs from './Outs';
import Vertical from './Vertical';
import Wire from './Wire';

export default function ExpectedApp(props) {
    return (
    <Xwrapper>
      <Horizontal>
        <Map className="io" name="ls">
          <Ins/>
          <Outs><div id="5"/></Outs>
        </Map>
        <Map className="io" name="x">
          <Ins/>
          <Outs><div id="x"/></Outs>
        </Map>
      </Horizontal>
      <Vertical>
        <Map name="Min-Max" > 
          <Ins><div id="9"/></Ins>
          <Outs><div id="0"/><div id="1"/></Outs>
        </Map>
        <Map infix={true} name="/">
          <Ins>
            <Map infix={true} name="+">
              <Ins>
                <div id="2"/>
                <div id="3"/>
              </Ins>
              <Outs/>
            </Map>
            <Map className="constant" name="2"/>
          </Ins>
          <Outs><div id="4"/></Outs>
        </Map>
      </Vertical>
      <Horizontal>
        <Map className="io" name="min">
          <Ins><div id="6"/></Ins>
          <Outs/>
        </Map>
        <Map className="io" name="avg">
          <Ins><div id="7"/></Ins>
          <Outs/>
        </Map>
        <Map className="io" name="avg">
          <Ins><div id="8"/></Ins>
          <Outs/>
        </Map>
      </Horizontal>
      <Wire start="0" end="2"/>
      <Wire start="1" end="3"/>
      <Wire start="5" end="9"/>
      <Wire start="0" end="6"/>
      <Wire start="4" end="7"/>
      <Wire start="1" end="8"/>

    </Xwrapper>);
}