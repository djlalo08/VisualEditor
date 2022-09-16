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
	<FileInput name="ls">{[":ix"]}</FileInput>
	<FileInput>{[":i1",":i0"]}</FileInput>
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
	<Map name="/" infix="true">
		<Ins infix="true">
			<Map name="+" infix="true">
				<Ins infix="true">
					<div id=":o0_0"/>
					<div id=":o1_0"/>
				</Ins>
				<Outs infix="true"/>
			</Map>
			<Map name="2" className="constant"/>
		</Ins>
		<Outs infix="true">
			<div id=":o2"/>
		</Outs>
	</Map>
</Vertical>
<Horizontal>
	<FileOutput name="min">{[":o0_1"]}</FileOutput>
	<FileOutput name="avg">{[":o2_0",":o1_1"]}</FileOutput>
	<FileOutput name="max">{[":o1_2"]}</FileOutput>
</Horizontal>

<Wire start=":i0" end=":i0_0"/>
<Wire start=":o0" end=":o0_0"/>
<Wire start=":o1" end=":o1_0"/>
<Wire start=":o0" end=":o0_1"/>
<Wire start=":o2" end=":o2_0"/>
<Wire start=":o1" end=":o1_1"/>
<Wire start=":o1" end=":o1_2"/>

    </Xwrapper>);
}