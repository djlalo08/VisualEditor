import Ins from "./Ins";
import Map from "./Map";
import Outs from "./Outs";

export default function FileInput(props){
    const {children, ...other} = props;
    return (<Map className="io" {...other}>
        <Ins/>
        <Outs x>{children}</Outs>
    </Map>);
}