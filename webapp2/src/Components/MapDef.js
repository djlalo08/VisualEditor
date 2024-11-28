import Node from "./Node";

export function MapDef(props){
    let {id, className, selected, children, other, name} = props;
    let [ins, outs, body] = children;
    let nameStyle = {padding: '0px 2px', margin: '1px', borderStyle: 'dashed'};
    if (selected){
        nameStyle.borderColor = 'rgb(184, 88, 88)';
        nameStyle.borderLeftColor = 'rgba(184, 88, 88, 0)';
        nameStyle.borderRightColor = 'rgba(184, 88, 88, 0)';
    } else {
        nameStyle.borderColor = 'rgba(184, 88, 88, 0)';
    }

    return (<div style={{'textAlign': 'left'}}>
        <span style={{display: 'flex', justifyContent: 'space-between', alignItems:'center'}}>
        {ins}
        <div style={nameStyle}>{name}</div>
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