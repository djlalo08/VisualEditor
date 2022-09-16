import Ins from "./Ins";
import Map from "./Map";
import Outs from "./Outs";

export default function FileInput(props){
    return (<Map className="io" name={props.name}>
        <Ins/>
        <Outs x>{props.children}</Outs>
    </Map>);
}