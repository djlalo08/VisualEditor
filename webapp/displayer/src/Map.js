import './App.css';
import Node from './Node.js';

export default function Map(props){
    
    let ins = props.ins ? props.ins.map((in_, index) => <Node key={index}>{in_}</Node>) : [];
    let outs = props.outs ? props.outs.map((out_, index) => <Node key={index}>{out_}</Node>) : [];

    return (<div id={props.id} className="Map">
        {ins}
        <div>{props.name}</div>
        {outs}
    </div>);
}
