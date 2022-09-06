import { intersperse } from '../Utils/ListUtils.js';
import Node from './Node.js';

export default function Map(props){
   
    let ins = props.ins ? props.ins.map((in_, index) => <Node key={index}>{in_}</Node>) : [];
    if (props.infix)
        ins = intersperse(ins, props.name);
    let outs = props.outs ? props.outs.map((out_, index) => <Node key={index}>{out_}</Node>) : [];

    return (<div id={props.id} className={props.className || "Map"}>
        {ins}
        {!props.infix && <div>{props.name}</div>}
        {outs}
    </div>);
}
