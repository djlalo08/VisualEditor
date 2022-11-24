
import { Xwrapper } from 'react-xarrows';
import FileInput from './FileInput';
import FileOutput from './FileOutput';
import Horizontal from './Horizontal';
import Ins from './Ins';
import Map from './Map';
import Node from './Node';
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
				<Node id={12}>
					<Map name="-" infix="true" id={13}>
						<Ins infix="true" id={14}>
							<Node id={15}>
								<Map name="sqr" id={16}>
									<Ins id={17}>
										<Node id={18}>
											<div id=":b_0"/>
										</Node>
									</Ins>
									<Outs id={20}/>
								</Map>
							</Node>
							<Node id={21}>
								<Map name="*" infix="true" id={22}>
									<Ins infix="true" id={23}>
										<Node id={24}>
											<Map name="4" className="constant" selected=" " id={25}/>
										</Node>
										<Node id={26}>
											<div id=":a_0"/>
										</Node>
										<Node id={28}>
											<div id=":c_0"/>
										</Node>
									</Ins>
									<Outs infix="true" id={30}/>
								</Map>
							</Node>
						</Ins>
						<Outs infix="true" id={31}/>
					</Map>
				</Node>
			</Ins>
			<Outs id={32}>
				<Node id={33}>
					<div id=":discr"/>
				</Node>
			</Outs>
		</Map>
	</Vertical>
	<Horizontal id={35}>
		<FileOutput id={36}>{[":discr_0"]}</FileOutput>
	</Horizontal>
</Root>

<Wire start=":b" end=":b_0"/>
<Wire start=":a" end=":a_0"/>
<Wire start=":c" end=":c_0"/>
<Wire start=":discr" end=":discr_0"/>
    </Xwrapper>);
}
