import { Xwrapper } from 'react-xarrows';
import FileInput from './FileInput';
import FileOutput from './FileOutput';
import Horizontal from './Horizontal';
import Ins from './Ins';
import Map from './Map';
import Outs from './Outs';
import Vertical from './Vertical';
import Wire from './Wire';

//I think the idea is that instead of updating the text in this app we have this return something different -- something that maps 
//And IR tree into a react tree...
export default function ExpectedApp(props) {
    return (
    <Xwrapper>
      <Horizontal>
        <FileInput name="ls">{["5"]}</FileInput>
        <FileInput name="unused">{["x", "y"]}</FileInput>
      </Horizontal>
      <Vertical>
        <Map name="Min-Max" > 
          <Ins x>{["9"]}</Ins>
          <Outs x>{["0", "1"]}</Outs>
        </Map>
        <Map infix={true} name="/">
          <Ins>
            <Map infix={true} name="+">
              <Ins x>{["2", "3"]}</Ins>
              <Outs/>
            </Map>
            <Map className="constant" name="2"/>
          </Ins>
          <Outs x>{["4"]}</Outs>
        </Map>
      </Vertical>
      <Horizontal>
        <FileOutput name="min">{["6"]}</FileOutput>
        <FileOutput name="avg">{["7"]}</FileOutput>
        <FileOutput name="max">{["8"]}</FileOutput>
      </Horizontal>
      <Wire start="0" end="2"/>
      <Wire start="1" end="3"/>
      <Wire start="5" end="9"/>
      <Wire start="0" end="6"/>
      <Wire start="4" end="7"/>
      <Wire start="1" end="8"/>

    </Xwrapper>);
}