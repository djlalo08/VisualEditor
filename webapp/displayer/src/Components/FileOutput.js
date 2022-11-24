import Ins from "./Ins";
import Map from "./Map";
import Outs from "./Outs";

export default function FileOutput(props){
    const {children, ...other} = props;
    return <Map className="io" {...other}>
        <Ins x>{children}</Ins>
        <Outs/>
    </Map>
}