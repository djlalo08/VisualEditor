import Node from "./Node";

export function MapDef(props){
    let {id, className, children, other, name} = props;
    let [ins, outs, body] = children;
    return (<div style={{'textAlign': 'left'}}>
        <span style={{display: 'flex', justifyContent: 'space-between', alignItems:'center'}}>
        {ins}
        {name}
        </span>
            <Node style={{borderStyle: 'inset'}}>
            {body}
            </Node>
        <div style={{display:'flex', justifyContent:'flex-end'}}>
            {outs}
        </div>
        <br/>
        <br/>
    </div>);
}