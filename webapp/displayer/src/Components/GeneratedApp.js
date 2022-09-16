import FileInput from './FileInput';
import FileOutput from './FileOutput';
import Horizontal from './Horizontal';
import Ins from './Ins';
import Map from './Map';
import Outs from './Outs';
import Vertical from './Vertical';

export default function GeneratedApp(){
    return( <>
<Horizontal>
	<FileInput>{[":i0"]}</FileInput>
	<FileInput>{[":i1",":ix"]}</FileInput>
</Horizontal>
<Vertical>
	<Map name="min-max">
		<Ins>
			<div id=":i0"/>
		</Ins>
		<Outs>
			<div name=":o0"/>
			<div name=":o1"/>
		</Outs>
	</Map>
	<Map name="div">
		<Ins>
			<Map name="add">
				<Ins>
					<div id=":o0"/>
					<div id=":o1"/>
				</Ins>
				<Outs/>
			</Map>
			<Map name="2"/>
		</Ins>
		<Outs>
			<div name=":o2"/>
		</Outs>
	</Map>
</Vertical>
<Horizontal>
	<FileOutput>{[":o0"]}</FileOutput>
	<FileOutput>{[":o2"]}</FileOutput>
	<FileOutput>{[":o1"]}</FileOutput>
</Horizontal>
    </>);

}