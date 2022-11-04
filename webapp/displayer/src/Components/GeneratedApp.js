
import { Xwrapper } from 'react-xarrows';
import FileInput from './FileInput';
import FileOutput from './FileOutput';
import Horizontal from './Horizontal';
import Ins from './Ins';
import Map from './Map';
import Outs from './Outs';
import Root from './Root';
import Vertical from './Vertical';
import Wire from './Wire';

export default function GeneratedApp(){
    return( <Xwrapper>
    
<Root id={1}>
	<Horizontal id={2}>
		<FileInput id={3}>{[":a"]}</FileInput>
		<FileInput id={5}>{[":b"]}</FileInput>
		<FileInput id={7}>{[":c"]}</FileInput>
	</Horizontal>
	<Vertical id={9}>
		<Map name="sqrt" id={10}>
			<Ins id={11}>
				<Map name="-" infix="true" id={12}>
					<Ins infix="true" id={13}>
						<Map name="sqr" id={14}>
							<Ins id={15}>
								<div id=":b_0"/>
							</Ins>
							<Outs id={17}/>
						</Map>
						<Map name="*" infix="true" id={18}>
							<Ins infix="true" id={19}>
								<Map name="4" className="constant" id={20}/>
								<div id=":a_0"/>
								<div id=":c_0"/>
							</Ins>
							<Outs infix="true" id={23}/>
						</Map>
					</Ins>
					<Outs infix="true" id={24}/>
				</Map>
			</Ins>
			<Outs id={25}>
				<div id=":discr"/>
			</Outs>
		</Map>
	</Vertical>
	<Horizontal id={27}>
		<FileOutput id={28}>{[":discr_0"]}</FileOutput>
	</Horizontal>
</Root>

<Wire start=":b" end=":b_0"/>
<Wire start=":a" end=":a_0"/>
<Wire start=":c" end=":c_0"/>
<Wire start=":discr" end=":discr_0"/>
    </Xwrapper>);
}
