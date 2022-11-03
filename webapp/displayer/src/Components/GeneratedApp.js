
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
    
<Root>
	<Horizontal>
		<FileInput>{[":a"]}</FileInput>
		<FileInput>{[":b"]}</FileInput>
		<FileInput>{[":c"]}</FileInput>
	</Horizontal>
	<Vertical>
		<Map name="sqrt">
			<Ins>
				<Map name="-" infix="true">
					<Ins infix="true">
						<Map name="sqr">
							<Ins>
								<div id=":b_0"/>
							</Ins>
							<Outs/>
						</Map>
						<Map name="*" infix="true">
							<Ins infix="true">
								<Map name="4" className="constant"/>
								<div id=":a_0"/>
								<div id=":c_0"/>
							</Ins>
							<Outs infix="true"/>
						</Map>
					</Ins>
					<Outs infix="true"/>
				</Map>
			</Ins>
			<Outs>
				<div id=":discr"/>
			</Outs>
		</Map>
	</Vertical>
	<Horizontal>
		<FileOutput>{[":discr_0"]}</FileOutput>
	</Horizontal>
</Root>

<Wire start=":b" end=":b_0"/>
<Wire start=":a" end=":a_0"/>
<Wire start=":c" end=":c_0"/>
<Wire start=":discr" end=":discr_0"/>
    </Xwrapper>);
}
