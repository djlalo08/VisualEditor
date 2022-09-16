import Ins from "./Ins";
import Map from "./Map";
import Outs from "./Outs";

export default function FileOutput(props){
    return <Map className="io" name={props.name}>
        <Ins x>{props.children}</Ins>
        <Outs/>
    </Map>
}