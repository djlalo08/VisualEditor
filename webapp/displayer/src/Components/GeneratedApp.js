import { Xwrapper } from 'react-xarrows';
import FileInput from './FileInput';
import FileOutput from './FileOutput';
import Horizontal from './Horizontal';
import Ins from './Ins';
import Map from './Map';
import Outs from './Outs';
import Vertical from './Vertical';
import Wire from './Wire';

export default function GeneratedApp(){
    return( <Xwrapper>
<Horizontal>
	<FileInput>{[":i0"]}</FileInput>
	<FileInput>{[":i1",":ix"]}</FileInput>
</Horizontal>
<Vertical>
	<Map name="min-max">
		<Ins>
			<div id=":i0_0"/>
		</Ins>
		<Outs>
			<div id=":o0"/>
			<div id=":o1"/>
		</Outs>
	</Map>
	<Map name="div">
		<Ins>
			<Map name="add">
				<Ins>
					<div id=":o0_0"/>
					<div id=":o1_0"/>
				</Ins>
				<Outs/>
			</Map>
			<Map name="2"/>
		</Ins>
		<Outs>
			<div id=":o2"/>
		</Outs>
	</Map>
</Vertical>
<Horizontal>
	<FileOutput>{[":o0_1"]}</FileOutput>
	<FileOutput>{[":o2_0"]}</FileOutput>
	<FileOutput>{[":o1_1"]}</FileOutput>
</Horizontal>

<Wire start=":i0" end=":i0_0"/>
<Wire start=":o0" end=":o0_0"/>
<Wire start=":o1" end=":o1_0"/>
<Wire start=":o0" end=":o0_1"/>
<Wire start=":o2" end=":o2_0"/>
<Wire start=":o1" end=":o1_1"/>

    </Xwrapper>);
}