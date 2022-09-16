import Horizontal from './Horizontal';
import Ins from './Ins';
import Map from './Map';
import Outs from './Outs';
import Vertical from './Vertical';

export default function GeneratedApp(){
    return( <>
<Horizontal>
	<div name=":i0"/>
	<div name=":i1"/>
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
	<div name=":o0"/>
	<div name=":o2"/>
	<div name=":o1"/>
</Horizontal>
    </>);

}